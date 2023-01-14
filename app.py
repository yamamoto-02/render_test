from flask import Flask,request,render_template,jsonify,Response
import re
app = Flask(__name__)

@app.route('/')
def main():
    return 'URLの後に　/v1/number2kanji/変換したい漢数字　or　/v1/kanji2number/変換したい漢数字'

@app.route('/v1/number2kanji/<num>')
def number2kanji(num):
    if num.isdigit() == True and 0<= int(num) <= 9999999999999999:
        kazu = ["","壱","弐","参","四","五","六","七","八","九"]
        kugiri_1 = ["","拾","百","千"]
        kugiri_2 = ["","万","億","兆"]

        num = list(map(int,list(str(num))))
        kansuji = []

        for k, v in zip(range(len(num)), reversed(num)) :
            keta = []
            keta.append(kazu[v if v>2 else 0 if k%4 else v])
            keta.append(kugiri_1[k%4 if v>0 else 0])
            keta.append((kugiri_2[0 if k%4 else int(k/4) if any(list(reversed(num))[k:(k+4 if len(num)>=(k+4) else len(num))]) else 0]))
            kansuji.append("".join(keta))

        kansuji = "".join(reversed(kansuji))
        return f'変換結果: {kansuji if kansuji else "零"}'

    else:
        return '', 204

    
@app.route('/v1/kanji2number/<kanji>')
def kanji2number(kanji):
    tt_ksuji = str.maketrans('一二三四五六七八九零壱弐参', '1234567890123')
    re_suji = re.compile(r'[十拾百千万億兆\d]+')
    re_kunit = re.compile(r'[十拾百千]|\d+')
    re_manshin = re.compile(r'[万億兆]|[^万億兆]+')

    TRANSUNIT = {'十': 10,'拾': 10,'百': 100,'千': 1000}
    TRANSMANS = {'万': 10000,'億': 100000000,'兆': 1000000000000}

    kstring = "'"+kanji+"'"
    sep = False
    def _transvalue(sj: str, re_obj=re_kunit, transdic=TRANSUNIT):
            unit = 1
            result = 0
            for piece in reversed(re_obj.findall(sj)):
                if piece in transdic:
                    if unit > 1:
                        result += unit
                    unit = transdic[piece]
                else:
                    val = int(piece) if piece.isdecimal() else _transvalue(piece)
                    result += val * unit
                    unit = 1

            if unit > 1:
                result += unit

            return result

    transuji = kstring.translate(tt_ksuji)

    for suji in sorted(set(re_suji.findall(transuji)), key=lambda s: len(s),
                            reverse=True):
            if not suji.isdecimal():
                arabic = _transvalue(suji, re_manshin, TRANSMANS)
                arabic = '{:,}'.format(arabic) if sep else str(arabic)
                transuji = transuji.replace(suji, arabic)
            elif sep and len(suji) > 3:
                transuji = transuji.replace(suji, '{:,}'.format(int(suji)))

    return f'変換結果: {transuji}'


if __name__ == "__main__":
    app.run(debug=True)

from bulb.utils.log import bulb_logger
from django import forms
import re


class OverloadedEmailField(forms.CharField):
    widget = forms.EmailInput
    default_validators = []

    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)


class AdminLoginForm(forms.Form):
    email = OverloadedEmailField(widget=forms.EmailInput(attrs={"id": "email",
                                                                "class": "input",
                                                                "spellcheck": "false",
                                                                "autocorrect": "off",
                                                                "placeholder": "Ex : john.dupont@mail.com"}),
                                 max_length=255,
                                 required=False,
                                 label="Email")

    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password",
                                                                 "class": "input",
                                                                 "spellcheck": "false",
                                                                 "autocorrect": "off",
                                                                 "placeholder": ""}),
                               max_length=255,
                               required=False,
                               label="Mot de passe")

    def clean_email(self):
        email_regex = "^([a-zA-Z0-9_%+](\.|\-)?){,249}[a-zA-Z0-9_%]@([a-zA-Z0-9_%+]\-?){,249}[a-zA-Z0-9_%]\.[a-z]{2,}$"
        email = self.cleaned_data.get("email")

        if not email:
            bulb_logger.error('ValidationError("Please enter an email address.")')
            raise forms.ValidationError("Please enter an email address.", code="invalid")

        if not re.fullmatch(email_regex, email) or 6 > len(email) > 255:
            bulb_logger.error('ValidationError("Please enter a valid email address.")')
            raise forms.ValidationError("Please enter a valid email address.", code="invalid")

        return email.lower()

    def clean_password(self):
        password_regex = "^(.*)?[૱┯┰┱┲❗►◄ĂăǕǖꞀ¤Ð¢℥Ω℧Kℶℷℸⅇ⅊⚌⚍⚎⚏⚭⚮⌀⏑⏒⏓⏔⏕⏖⏗⏘⏙⏠⏡⏦ᶀᶁᶂᶃᶄᶆᶇᶈᶉᶊᶋᶌᶍᶎᶏᶐᶑᶒᶓᶔᶕᶖᶗᶘᶙᶚᶸᵯᵰᵴᵶᵹᵼᵽᵾᵿ  ‎‏ ⁁⁊ ⁪⁫⁬⁭⁮⁯⸜⸝¶¥£⅕⅙⅛⅔⅖⅗⅘⅜⅚⅐⅝↉⅓⅑⅒⅞←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯↰↱↲↳↴↵↶↷↸↹↺↻↼↽↾↿⇀⇁⇂⇃⇄⇅⇆⇇⇈⇉⇊⇋⇌⇍⇎⇏⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙⇚⇛⇜⇝⇞⇟⇠⇡⇢⇣⇤⇥⇦⇨⇩⇪⇧⇫⇬⇭⇮⇯⇰⇱⇲⇳⇴⇵⇶⇷⇸⇹⇺⇻⇼⇽⇾⇿⟰⟱⟲⟳⟴⟵⟶⟷⟸⟹⟺⟻⟼⟽⟾⟿⤀⤁⤂⤃⤄⤅⤆⤇⤈⤉⤊⤋⤌⤍⤎⤏⤐⤑⤒⤓⤔⤕⤖⤗⤘⤙⤚⤛⤜⤝⤞⤟⤠⤡⤢⤣⤤⤥⤦⤧⤨⤩⤪⤫⤬⤭⤮⤯⤰⤱⤲⤳⤴⤵⤶⤷⤸⤹⤺⤻⤼⤽⤾⤿⥀⥁⥂⥃⥄⥅⥆⥇⥈⥉⥊⥋⥌⥍⥎⥏⥐⥑⥒⥓⥔⥕⥖⥗⥘⥙⥚⥛⥜⥝⥞⥟⥠⥡⥢⥣⥤⥥⥦⥧⥨⥩⥪⥫⥬⥭⥮⥯⥰⥱⥲⥳⥴⥵⥶⥷⥸⥹⥺⥻⥼⥽⥾⥿➔➘➙➚➛➜➝➞➝➞➟➠➡➢➣➤➥➦➧➨➩➩➪➫➬➭➮➯➱➲➳➴➵➶➷➸➹➺➻➼➽➾⬀⬁⬂⬃⬄⬅⬆⬇⬈⬉⬊⬋⬌⬍⬎⬏⬐⬑☇☈⏎⍃⍄⍅⍆⍇⍈⍐⍗⍌⍓⍍⍔⍏⍖♾⎌☊☋☌☍⌃⌄⌤⌅⌆⌇⚋⚊⌌⌍⌎⌏⌐⌑⌔⌕⌗⌙⌢⌣⌯⌬⌭⌮⌖⌰⌱⌲⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⍯⍰⌽⌾⌿⍀⍁⍂⍉⍊⍋⍎⍏⍑⍒⍕⍖⍘⍙⍚⍛⍜⍝⍞⍠⍟⍡⍢⍣⍤⍥⍨⍩⍦⍧⍬⍿⍪⍮⍫⍱⍲⍭⍳⍴⍵⍶⍷⍸⍹⍺⍼⍽⍾⎀⎁⎂⎃⎄⎅⎆⎉⎊⎋⎍⎎⎏⎐⎑⎒⎓⎔⎕⏣⌓⏥⏢⎖⎲⎳⎴⎵⎶⎸⎹⎺⎻⎼⎽⎾⎿⏀⏁⏂⏃⏄⏅⏆⏇⏈⏉⏉⏋⏌⏍⏐⏤⏚⏛Ⓝℰⓦ!   ⌘«»‹›‘’“”„‚❝❞£¥€$¢¬¶@§®©™°×π±√‰Ω∞≈÷~≠¹²³½¼¾‐–—|⁄\[\]{}†‡…·•●⌥⌃⇧↩¡¿‽⁂∴∵◊※←→↑↓☜☞☝☟✔★☆♺☼☂☺☹☃✉✿✄✈✌✎♠♦♣♥♪♫♯♀♂αßÁáÀàÅåÄäÆæÇçÉéÈèÊêÍíÌìÎîÑñÓóÒòÔôÖöØøÚúÙùÜüŽž₳฿￠€₡¢₢₵₫￡£₤₣ƒ₲₭₥₦₱＄$₮₩￦¥￥₴₰¤៛₪₯₠₧₨௹﷼㍐৲৳~ƻƼƽ¹¸¬¨ɂǁ¯Ɂǂ¡´°ꟾ¦}{|\.,·\]\)\[/_\¿º§\"\*\-\+\(!&%$¼¾½¶©®@ẟⱿ`Ȿ^꜠꜡ỻ'=:;<ꞌꞋ꞊ꞁꞈ꞉>?÷ℾℿ℔℩℉⅀℈þðÞµªꝋꜿꜾⱽⱺⱹⱷⱶⱵⱴⱱⱰⱦȶȴȣȢȡȝȜțȋȊȉȈǯǮǃǀƿƾƺƹƸƷƲưƪƣƢƟƛƖƕƍſỽ⸀⸁⸂⸃⸄⸅⸆⸇⸈⸉⸊⸋⸌⸍⸎⸏⸐⸑⸒⸔⸕▲▼◀▶◢◣◥◤△▽◿◺◹◸▴▾◂▸▵▿◃▹◁▷◅▻◬⟁⧋⧊⊿∆∇◭◮⧩⧨⌔⟐◇◆◈⬖⬗⬘⬙⬠⬡⎔⋄◊⧫⬢⬣▰▪◼▮◾▗▖■∎▃▄▅▆▇█▌▐▍▎▉▊▋❘❙❚▀▘▝▙▚▛▜▟▞░▒▓▂▁▬▔▫▯▭▱◽□◻▢⊞⊡⊟⊠▣▤▥▦⬚▧▨▩⬓◧⬒◨◩◪⬔⬕❏❐❑❒⧈◰◱◳◲◫⧇⧅⧄⍁⍂⟡⧉○◌◍◎◯❍◉⦾⊙⦿⊜⊖⊘⊚⊛⊝●⚫⦁◐◑◒◓◔◕⦶⦸◵◴◶◷⊕⊗⦇⦈⦉⦊❨❩⸨⸩◖◗❪❫❮❯❬❭❰❱⊏⊐⊑⊒◘◙◚◛◜◝◞◟◠◡⋒⋓⋐⋑╰╮╭╯⌒╳✕╱╲⧸⧹⌓◦❖✖✚✜⧓⧗⧑⧒⧖_⚊╴╼╾‐⁃ ‒\-–⎯—―╶╺╸─━┄┅┈┉╌╍═≣≡☰☱☲☳☴☵☶☷╵╷╹╻│▕▏┃┆┇┊╎┋╿╽┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╏║╔╒╓╕╖╗╚╘╙╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬⌞⌟⌜⌝⌊⌋⌉⌈⌋₯ἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏἐἑἒἓἔἕἘἙἚἛἜἝἠἡἢἣἤἥἦἧἨἩἪἫἬἭἮἯἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὀὁὂὃὄὅὈὉὊὋὌὍὐὑὒὓὔὕὖὗὙὛὝὟὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὰάὲέὴήὶίὸόὺύὼώᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼ᾽ι᾿῀῁ῂῃῄῆῇῈΈῊΉῌ῍῎῏ῐῑῒΐῖῗῘῙῚΊ῝῞῟ῠῡῢΰῤῥῦῧῨῩῪΎῬ῭΅`ῲῳῴῶῷῸΌῺΏῼ´῾ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿⒶⓐ⒜ẠạẢảḀḁÂÃǍǎẤấẦầẨẩȂȃẪẫẬậÀÁẮắẰằẲẳẴẵẶặĀāĄąǞȀȁÅǺǻÄäǟǠǡâáåãàẚȦȧȺÅⱥÆæǼǢǣⱯꜲꜳꜸꜺⱭꜹꜻª℀⅍℁Ⓑⓑ⒝ḂḃḄḅḆḇƁɃƀƃƂƄƅℬⒸⓒ⒞ḈḉĆćĈĉĊċČčÇçƇƈȻȼℂ℃ℭƆ℅℆℄ꜾꜿⒹⓓ⒟ḊḋḌḍḎḏḐḑḒḓĎďƊƋƌƉĐđȡⅅⅆǱǲǳǄǅǆȸⒺⓔ⒠ḔḕḖḗḘḙḚḛḜḝẸẹẺẻẾếẼẽỀềỂểỄễỆệĒēĔĕĖėĘęĚěÈèÉéÊêËëȄȅȨȩȆȇƎⱸɆℇℯ℮ƐℰƏǝⱻɇⒻⓕ⒡ḞḟƑƒꜰℲⅎꟻℱ℻Ⓖⓖ⒢ƓḠḡĜĝĞğĠġĢģǤǥǦǧǴℊ⅁ǵⒽⓗ⒣ḢḣḤḥḦḧḨḩḪḫẖĤĥȞȟĦħⱧⱨꜦℍǶℏℎℋℌꜧⒾⓘ⒤ḬḭḮḯĲĳìíîïÌÍÎÏĨĩĪīĬĭĮįıƗƚỺǏǐⅈⅉℹℑℐⒿⓙ⒥ĴĵȷⱼɈɉǰⓀⓚ⒦ḰḱḲḳḴḵĶķƘƙꝀꝁꝂꝃꝄꝅǨǩⱩⱪĸⓁⓛ⒧ḶḷḸḹḺḻḼḽĹĺĻļĽİľĿŀŁłỈỉỊịȽⱠꝈꝉⱡⱢꞁℒǇǈǉ⅃⅂ℓȉȈȊȋⓂⓜ⒨ḾḿṀṁṂṃꟿꟽⱮƩƜℳⓃⓝ⒩ṄṅṆṇṈṉṊṋŃńŅņŇňǸǹŊƝñŉÑȠƞŋǊǋǌȵℕ№ṌṍṎṏṐṑṒṓȪȫȬȭȮȯȰȱǪǫǬǭỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợƠơŌōŎŏŐőÒÓÔÕÖǑȌȍȎȏŒœØǾꝊǽǿℴ⍥⍤Ⓞⓞ⒪òóôõöǒøꝎꝏⓅⓟ⒫℗ṔṕṖṗƤƥⱣℙǷꟼ℘Ⓠⓠ⒬Ɋɋℚ℺ȹⓇⓡ⒭ŔŕŖŗŘřṘṙṚṛṜṝṞṟȐȑȒȓɍɌƦⱤ℞Ꝛꝛℜℛ℟ℝⓈⓢ⒮ṠṡṢṣṤṥṦṧṨṩŚśŜŝŞşŠšȘșȿꜱƧƨẞßẛẜẝ℠Ⓣⓣ⒯ṪṫṬṭṮṯṰṱŢţŤťŦŧƬƮẗȚȾƫƭțⱦȶ℡™Ⓤⓤ⒰ṲṳṴṵṶṷṸṹṺṻỤỦủỨỪụứỬửừữỮỰựŨũŪūŬŭŮůŰűǙǚǗǘǛǜŲųǓǔȔȕÛûȖȗÙùÜüƯúɄưƲƱⓋⓥ⒱ṼṽṾṿỼɅ℣ⱱⱴⱽⓌⓦ⒲ẀẁẂẃẄẅẆẇẈẉŴŵẘⱲⱳⓍⓧ⒳ẊẋẌẍℵ×Ⓨⓨ⒴ẎẏỾỿẙỲỳỴỵỶỷỸỹŶŷƳƴŸÿÝýɎɏȲƔ⅄ȳℽⓏⓩ⒵ẐẑẒẓẔẕŹźŻżŽžȤȥⱫⱬƵƶɀℨℤ⟀⟁⟂⟃⟄⟇⟈⟉⟊⟐⟑⟒⟓⟔⟕⟖⟗⟘⟙⟚⟛⟜⟝⟞⟟⟠⟡⟢⟣⟤⟥⟦⟧⟨⟩⟪⟫⦀⦁⦂⦃⦄⦅⦆⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⦙⦚⦛⦜⦝⦞⦟⦠⦡⦢⦣⦤⦥⦦⦧⦨⦩⦪⦫⦬⦭⦮⦯⦰⦱⦲⦳⦴⦵⦶⦷⦸⦹⦺⦻⦼⦽⦾⦿⧀⧁⧂⧃⧄⧅⧆⧇⧈⧉⧊⧋⧌⧍⧎⧏⧐⧑⧒⧓⧔⧕⧖⧗⧘⧙⧚⧛⧜⧝⧞⧟⧡⧢⧣⧤⧥⧦⧧⧨⧩⧪⧫⧬⧭⧮⧯⧰⧱⧲⧳⧴⧵⧶⧷⧸⧹⧺⧻⧼⧽⧾⧿∀∁∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿≀≁≂≃≄≅≆≇≈≉≊≋≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≤≥≦≧≨≩≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿✕✖✚◀▶❝❞★☆☼☂☺☹✄✈✌✎♪♫☀☁☔⚡❆☽☾✆✔☯☮☠⚑☬✄✏♰✡✰✺⚢⚣♕♛♚♬ⓐⓑⓒⓓ↺↻⇖⇗⇘⇙⟵⟷⟶⤴⤵⤶⤷➫➬€₤＄₩₪⟁⟐◆⎔░▢⊡▩⟡◎◵⊗❖ΩβΦΣΞ⟁⦻⧉⧭⧴∞≌⊕⋍⋰⋱✖⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾ᴕ⸨⸩❪❫⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛⓪①②③④⑤⑥⑦⑧⑨⑩➀➁➂➃➄➅➆➇➈➉⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⓿❶❷❸❹❺❻❼❽❾❿➊➋➌➍➎➏➐➑➒➓⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇ᶅᶛᶜᶝᶞᶟᶠᶡᶢᶣᶤᶥᶦᶧᶨᶩᶪᶫᶬᶭᶮᶯᶰᶱᶲᶳᶴᶵᶶᶷᶹᶺᶻᶼᶽᶾᶿᴀᴁᴂᴃᴄᴅᴆᴇᴈᴉᴊᴋᴌᴍᴎᴏᴐᴑᴒᴓᴔᴕᴖᴗᴘᴙᴚᴛᴜᴝᴞᴟᴠᴡᴢᴣᴤᴥᴦᴧᴨᴩᴪᴫᴬᴭᴮᴯᴰᴱᴲᴳᴴᴵᴶᴷᴸᴹᴺᴻᴼᴽᴾᴿᵀᵁᵂᵃᵄᵅᵆᵇᵈᵉᵊᵋᵌᵍᵎᵏᵐᵑᵒᵓᵔᵕᵖᵗᵘᵙᵚᵛᵜᵝᵞᵟᵠᵡᵢᵣᵤᵥᵦᵧᵨᵩᵪᵫᵬᵭᵮᵱᵲᵳᵵᵷᵸᵺᵻ ᷋ ᷌ ᷍ ᷎ ᷏ ᷓ ᷔ ᷕ ᷖ ᷗ ᷘ ᷙ ᷛ ᷜ ᷝ ᷞ ᷟ ᷠ ᷡ ᷢ ᷣ ᷤ ᷥ ᷦ‘’‛‚“”„‟«»‹›Ꞌ\"❛❜❝❞<>@‧¨․꞉:⁚⁝⁞‥…⁖⸪⸬⸫⸭⁛⁘⁙⁏;⦂⁃‐ ‒\-–⎯—―_⁓⸛⸞⸟ⸯ¬/\⁄\⁄|⎜¦‖‗†‡·•⸰°‣⁒%‰‱&⅋§÷\+±=꞊′″‴⁗‵‶‷‸\*⁑⁎⁕※⁜⁂!‼¡?¿⸮⁇⁉⁈‽⸘¼½¾²³©®™℠℻℅℁⅍℄¶⁋❡⁌⁍⸖⸗⸚⸓\(\)\[\]{}⸨⸩❨❩❪❫⸦⸧❬❭❮❯❰❱❴❵❲❳⦗⦘⁅⁆〈〉⏜⏝⏞⏟⸡⸠⸢⸣⸤⸥⎡⎤⎣⎦⎨⎬⌠⌡⎛⎠⎝⎞⁀⁔‿⁐‾⎟⎢⎥⎪ꞁ⎮⎧⎫⎩⎭⎰⎱✈☀☼☁☂☔⚡❄❅❆☃☉☄★☆☽☾⌛⌚☇☈⌂⌁✆☎☏☑✓✔⎷⍻✖✗✘☒✕☓☕♿✌☚☛☜☝☞☟☹☺☻☯⚘☮✝⚰⚱⚠☠☢⚔⚓⎈⚒⚑⚐☡❂⚕⚖⚗✇☣⚙☤⚚⚛⚜☥☦☧☨☩†☪☫☬☭✁✂✃✄✍✎✏✐✑✒✉✙✚✜✛♰♱✞✟✠✡☸✢✣✤✥✦✧✩✪✫✬✭✮✯✰✲✱✳✴✵✶✷✸✹✺✻✼✽✾❀✿❁❃❇❈❉❊❋⁕☘❦❧☙❢❣♀♂⚢⚣⚤⚦⚧⚨⚩☿♁⚯♔♕♖♗♘♙♚♛♜♝♞♟☖☗♠♣♦♥❤❥♡♢♤♧⚀⚁⚂⚃⚄⚅⚇⚆⚈⚉♨♩♪♫♬♭♮♯⌨⏏⎗⎘⎙⎚⌥⎇⌘⌦⌫⌧♲♳♴♵♶♷♸♹♺♻♼♽⁌⁍⎌⌇⌲⍝⍟⍣⍤⍥⍨⍩⎋♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓⏚⏛| | | || | | | | ||](.*)?$"
        password = self.cleaned_data.get("password")

        if not password:
            bulb_logger.error('ValidationError("Please enter a password."')
            raise forms.ValidationError("Please enter a password.", code="invalid")

        if not re.fullmatch(password_regex, password) or not re.fullmatch("^(.*)?\d(.*)?$", password) or 10 > len(
                password) > 255:
            bulb_logger.error('ValidationError("Please enter a valid password."')
            raise forms.ValidationError("Please enter a valid password.", code="invalid")

        return password

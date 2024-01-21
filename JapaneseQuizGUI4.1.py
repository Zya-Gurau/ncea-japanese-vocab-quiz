import random
import time
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
import os, sys
from kivy.resources import resource_add_path, resource_find
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
import atexit
import pickle
Window.clearcolor = (1, 1, 1, 1)

#Notes:
#Because kivy cannot  display japanese text within it's own code, any japanese that needs to displayed must be assigned to a
#variable which is then passed through to the kivy side of the program

# The strings in the word lists are structured with the japanese word and the english counterpart seperated by a space 
# the two ords are seperateed into the display word and the answer during processing.


# This list contains all of the NCEA level one words both japanese and english
LevelOneWordList = [    
    "アイスクリーム ice_cream",
    "あいだ between",
    "あう to_meet",
    "あおい blue",
    "あかい red",
    "あき autumn",
    "あける to_open",
    "あげる to_give/raise",
    "あさ morning",
    "あさごはん breakfast",
    "あさって the_day_after_tomorrow",
    "あし foot/leg",
    "あした tomorrow",
    "あそこ over_there",
    "あそぶ to_play",
    "あたま head",
    "あたたかい warm",
    "あたらしい new",
    "あつい hot",
    "あと after",
    "あなた you",
    "あに (one's_own_)_older_brother",
    "あね (one's_own)_older_sister",
    "アパート apartment",
    "あまり not_much",
    "あめ rain",
    "あらう to_wash",
    "ある to_be_(inanimate)",
    "あるく to_walk",
    "あれ that_over_there",
    "いい；よい good",
    "いいえ no",
    "いえ house",
    "イギリス England",
    "いく to_go",
    "いくら how_much_?",
    "いっしょ together",
    "いす chair",
    "いたい sore",
    "いちご strawberry",
    "いちばん number_one", 
    "いつ when_?",
    "いつも always",
    "いとこ cousin",
    "いなか the_countryside",
    "いぬ dog",
    "いま now",
    "いま living_room",
    "いもうと younger_sister",
    "いや unpleasant",
    "いる to_be_(animate)",
    "いれる to_put_inside",
    "いろ colour",
    "いろいろ various",
    "うえ above",
    "うし cow",
    "うしろ behind",
    "うた song",
    "うたう to_sing",
    "うち home",
    "うま horse",
    "うみ sea",
    "うる to_sell",
    "うるさい noisy",
    "うんどう exercise",
    "うんてん drive",
    "え picture",
    "えいが movie",
    "えいがかん movie_theatre",
    "えいご English",
    "ええ yes",
    "えき station",
    "えんぴつ pencil",
    "おいしい delicious",
    "おいしゃ doctor",
    "おおきい  big",
    "オーストラリア Australia",
    "おかあさん mother",
    "おかし sweets",
    "おかね money",
    "おかしい funny",
    "おきる to_get_up",
    "おきゃく customer",
    "おくれる to_be_late",
    "さけ alcohol",
    "さら plate",
    "おじ uncle",
    "おじいさん grandfather",
    "おそい slow",
    "おちゃ green_tea",
    "おつり change_(money)",
    "おてら temple",
    "おとうさん father",
    "おとうと younger_brother",
    "おとこ boy",
    "おととい the_day_before_yesterday",
    "おとな adult",
    "おなか stomach",
    "なまえ name",
    "おにいさん older_brother",
    "おねえさん older_sister",
    "おば aunt",
    "おばあさん grandmother",
    "おはし chopsticks",
    "おふろ bath",
    "おふろば bath_room",
    "おべんとう packed_lunch",
    "おみやげ souvenir",
    "おみやげや souvenir_shop",
    "おもい heavy",
    "おもしろい interesting",
    "おりる to_get_off_(transport)",
    "おわり end",
    "おわる to_finish",
    "おんがく music",
    "おんな girl",
    "かいしゃ company",
    "かいもの shopping",
    "かう to_buy",
    "かえる to_return",
    "かお face",
    "かかる to_take_(time/money)",
    "かく to_write",
    "がくせい student",
    "かぜ wind",
    "かぞく family",
    "かっこいい good_looking",
    "がっこう school",
    "かど corner",
    "かばん bag",
    "かぶる to_wear_(on_head)",
    "かみ paper",
    "かみのけ hair",
    "かもく school_subject",
    "かようび Tuesday",
    "かるい light_(weight)",
    "ガレージ garage",
    "カレーライス curry_&_rice",
    "かわ river",
    "かわいい cute",
    "かんこく Korea",
    "かんごし nurse",
    "かんたん easy",
    "がんばる try_hard",
    "き tree",
    "キーウィー Kiwifruit/kiwi",
    "きいろ yellow",
    "きく to_listen",
    "ギター guitar",
    "きたない dirty",
    "きっさてん coffee_shop",
    "きっぷ ticket",
    "きのう yesterday",
    "きもの kimono",
    "キャンプ camp",
    "きょう today",
    "きょうかい church",
    "きょうしつ classroom",
    "きょうだい siblings",
    "きょねん last_year",
    "きらい dislike",
    "きる to_wear_(from_the_shoulder)",
    "きれい beautiful",
    "ぎんこう bank",
    "きんようび Friday",
    "くうこう airport",
    "くすり medicine", 
    "くすりや chemist",
    "くだもの fruit",
    "くち mouth",
    "くつ shoe", 
    "くつや shoe_shop",
    "くつした socks",
    "くもり cloudy",
    "ぐらい about",
    "グラウンド grounds",
    "クラス class",
    "クラブかつどう club_activities",
    "クリケット cricket",
    "クリスマス Christmas",
    "くる to_come",
    "くるま car",
    "くろい black",
    "けいたい cellphone",
    "けさ this_morning",
    "けしゴム rubber",
    "げつようび Monday",
    "げんかん genkan",
    "げんき healthy",
    "けんぶつ sightseeing",
    "こうえん park",
    "こうこうせい senior_high_school_student",
    "こうさてん intersection",
    "こうちょうせんせい school_principal",
    "こうこう senior_high_school",
    "こうちゃ tea",
    "コーヒー coffee",
    "コーラ Coke",
    "ここ here",
    "ごご afternoon",
    "ごぜん a.m.",
    "ことし this_year",
    "こども child",
    "ごはん cooked_rice",
    "ごみ rubbish",
    "ごみばこ rubbish_bin",
    "こむ to_be_crowded",
    "ゴルフ golf",
    "これ this",
    "ごろ about_(time)",
    "こんげつ this_month",
    "コンサート concert",
    "こんしゅう this_week",
    "こんばん this_evening",
    "サーフィン surfing",
    "さかな fish", 
    "さかなや fish_shop",
    "さくら cherry_blossoms",
    "さしみ sashimi", 
    "ざっし magazine",
    "サッカー soccer",
    "さとう sugar",
    "さむい cold",
    "サラダ salad",
    "サンドイッチ sandwich",
    "さんぽ walk",
    "しあい competition",
    "しけん examination",
    "しょうかい introduction",
    "じこしょうかい self_introduction",
    "しごと job",
    "しずか quiet",
    "した under",
    "じてんしゃ bicycle",
    "しめる to_close",
    "しゃかい society",
    "じゃがいも potato",
    "しゃしん photograph",
    "シャツ shirt",
    "シャワー shower",
    "しゅうまつ weekend",
    "しゅくだい homework",
    "しゅふ housewife",
    "しゅみ hobby", 
    "しょうがくせい primary_school_student",
    "しょうがっこう primary_school",
    "じょうず skilful",
    "しる to_know",
    "しろい white",
    "しんかんせん bullet_train",
    "しんごう traffic_lights",
    "しんしつ bedroom",
    "じんじゃ shrine",
    "しんぶん newspaper",
    "すいえい swimming",
    "すいか watermelon",
    "すいようび Wednesday",
    "すうがく mathematics",
    "スーパー supermarket",
    "スカート skirt",
    "すき like",
    "すごい great",
    "すこし a_little_bit",
    "すずしい cool",
    "ステーキ steak",
    "スペイン Spain",
    "スプーン spoon",
    "スポーツ sports",
    "ズボン trousers",
    "すむ to live",
    "スリッパ slippers",
    "する to_do",
    "すわる to_sit",
    "せがたかい tall",
    "がひくい short",
    "せいと pupil",
    "せいふく uniform",
    "セーター jersey",
    "せまい narrow",
    "せんげつ last_month",
    "せんしゅう last_week",
    "せんせい teacher",
    "ぜんぜん never",
    "せんたく washing",
    "ぜんぶ all",
    "そうじ cleaning",
    "そこ there",
    "そして and",
    "そと outside",
    "そば nearby",
    "それ that",
    "それから and_then",
    "たいいく physical_education", 
    "たいいくかん gymnasium",
    "だいがく university",
    "だいがくせい university_student",
    "だいじょうぶ all_right",
    "たいせつ important",
    "たいてい usually",
    "だいどころ kitchen",
    "たいへん a_burden",
    "たかい tall",
    "たくさん a_lot",
    "だけ only",
    "たつ to_stand",
    "たのしい enjoyable",
    "たべもの food",
    "たべる to_eat",
    "たまご egg",
    "だめ no_good",
    "だれ who_?",
    "たんじょうび birthday",
    "ちいさい small",
    "ちかい near",
    "ちかてつ subway",
    "ちず map",
    "ちち (my)_father",
    "ちゃいろい brown",
    "ちゃわん bowl",
    "ちゅうがくせい junior_high_school_student",
    "ちゅうがこっう junior_high_school",
    "ちゅうごく China",
    "ちょっと a_bit",
    "ちり geography",
    "つかう to_use",
    "つかれる to_get_tired",
    "つぎ next",
    "つく to_arrive",
    "つくえ desk",
    "つくる to_make",
    "つまらない boring",
    "つよい strong",
    "つり fishing",
    "て hand",
    "テーブル table",
    "てがみ letter",
    "できる to_be_able_to_do",
    "デザート dessert",
    "デパート department_store",
    "でる to_leave",
    "テレビ television",
    "てんき weather",
    "でんしゃ train",
    "でんわ telephone",
    "ドイツ Germany",
    "トイレ toilet",
    "どう how_?",
    "どうきゅうせい classmate",
    "どうぶつ animal", 
    "どうぶつえん zoo",
    "とおい far_away",
    "トースト toast",
    "ときどき sometimes",
    "とくい good_at",
    "とけい watch",
    "どこ where_?",
    "ところ place",
    "としょかん library",
    "とだな cupboard",
    "とても very",
    "となり next_to",
    "とまる to_stay", 
    "ともだち friend",
    "どようび Saturday",
    "ドライブ drive",
    "とり bird",
    "とる to_take",
    "ナイフ knife",
    "なおる to_heal",
    "なか inside",
    "ながい long",
    "なつ summer",
    "なに what_?",
    "ならう to_learn",
    "なる to become",
    "にがて not_good_at",
    "にぎやか lively",
    "にく meat", 
    "にくや butcher's_shop",
    "にちようび Sunday",
    "にほん Japan",
    "にもつ luggage",
    "ニュージーランド New_Zealand",
    "にわ garden",
    "ぬぐ to_take_off",
    "ネクタイ necktie",
    "ねこ cat",
    "ネットボール netball",
    "ねむい sleepy",
    "ねる to_lie_down",
    "のうじょう farm",
    "ノート exercise_book",
    "のぼる to_climb",
    "のみもの drink",
    "のむ to_drink",
    "のる to_get_on",
    "は tooth",
    "パーティー party",
    "はい yes",
    "バイク motor_bike",
    "はいる to_enter",
    "はく to_wear_(below_the_waist)",
    "はこ box",
    "はし bridge",
    "はしる to_run",
    "はじまる to_begin",
    "はじめ beginning",
    "バスてい bus_stop",
    "バスケットボール basketball",
    "パソコン computer",
    "はたらく to_work",
    "はな flower",
    "はな nose",
    "はなし story/speech",
    "はなす to_speak",
    "はは (my)_mother",
    "はやい early/fast",
    "はる spring",
    "はれ fine_weather",
    "バレーボール volleyball",
    "ばんごう number",
    "ばんごはん dinner",
    "ハンバーガー hamburger",
    "ひく to_play_(a_stringed_instrument)",
    "ひくい short", 
    "ピクニック picnic",
    "ひこうき plane",
    "びじゅつ art",
    "ひだり left",
    "ひつじ sheep",
    "ひと person",
    "ひま free_time",
    "びょういん hospital",
    "びょうき sick",
    "ひる day_time",
    "ビル building",
    "ひるごはん lunch",
    "ひろい wide",
    "ピンク pink",
    "プール pool",
    "フォーク fork",
    "ふとる to_put_on_weight",
    "ふでばこ pencil_case",
    "ふね boat",
    "ふべん inconvenient",
    "ふゆ winter",
    "ブラウス blouse",
    "フランス France",
    "ふるい old", 
    "へた bad_at",
    "ペット pet",
    "ベッド bed",
    "へや room",
    "へん strange",
    "べんきょう study",
    "べんり convenient",
    "ぼうし hat",
    "ホームルーム home_room",
    "ぼく me_(for_males)",
    "ほしい want",
    "ホッケー hockey",
    "ホワイトボード white_board",
    "ほん book",
    "ほんや book_shop",
    "ほんだな bookcase",
    "まいあさ every_morning",
    "まいしゅう every_week",
    "まいつき every_month",
    "まいとし every_year",
    "まいにち every_day",
    "まいばん every_evening",
    "まえ  before",
    "マオリ Maori",
    "まがる to_turn",
    "まずい awful_taste",
    "また again",
    "まち town",
    "まつ to_wait",
    "まっすぐ straight_ahead",
    "まど window",
    "まんが comic",
    "マンション large_apartment",
    "みえる can_see",
    "みかん mandarin",
    "みぎ right", 
    "みじかい short", 
    "みず 水 water",
    "みずうみ lake",
    "みせ shop",
    "みせる to_show",
    "みち street",
    "みどり green",
    "みみ ear",
    "みなさん everyone",
    "みる to_see",
    "ミルク milk",
    "むずかしい difficult",
    "め eye",
    "めがね glasses",
    "メニュー menu",
    "もくようび Thursday",
    "もっていく To_take",
    "もってくる to_bring", 
    "もらう to_receive",
    "もり forest",
    "やおや vegetable_shop",
    "やきゅう baseball",
    "やさい vegetable",
    "やさしい kind",
    "やすい cheap",
    "やすみ a_break",
    "やすむ to_have_a_break",
    "やせる to_lose_weight",
    "やま mountain",
    "やまのぼり mountain_climbing",
    "やめる to_stop",
    "ゆうびんきょく post_office",
    "ゆうめい famous",
    "ゆき snow",
    "ようふく clothes",
    "よく often",
    "よこ beside",
    "よむ to_read",
    "よる evening",
    "らいげつ next_month",
    "らいしゅう next_week",
    "らいねん next_year",
    "ラグビー rugby",
    "りか science",
    "りょうり cooking",
    "れきし history",
    "レストラン restaurant",
    "れんしゅう practice",
    "レンタカー rental_car",
    "わかる to_understand",
    "わすれる to_forget",
    "わたし 私 me",
    "わたる to_cross",
    "わるい bad",
    "ワンピース dress"]

# This list contains all of the NCEA level two words both japanese and english
LevelTwoWordList = [
    "あいさつ greetings",
    "ごあいさつする to_greet",
    "あかちゃん baby",
    "あがる  to_go_up/to_enter_(house)",
    "あかるい light/bright",
    "あぶない dangerous",
    "あんぜん safety",
    "いう to_say",
    "いそがしい busy",
    "いっしょうけんめい diligently",
    "いっぱい full",
    "いりぐち entrance",
    "うける  to_receive",
    "うりば sales_counter",
    "うれしい to_be_glad",
    "うんどうかい sports_day",
    "エアコン air-conditioning",
    "えさ pet_food",
    "えらぶ to_choose",
    "おうえんする to_support",
    "おくる to_send",
    "こめ uncooked_rice",
    "おこる to_get_angry",
    "おちる to fall; to fail",
    "おとなしい well-behaved",
    "おなじ the_same",
    "おもう to_think",
    "おや parent(s)",
    "おゆ hot_water",
    "およぐ to_swim",
    "がいこく foreign_country",
    "がいこくじん foreigner",
    "かいだん staircase",
    "かがく Chemistry",
    "かぎ key",
    "かさ umbrella",
    "かじ housework",
    "かす to_lend",
    "かたづける to_tidy_up",
    "かつ to_win",
    "がっき school_term",
    "かならず always",
    "からだ body",
    "かりる to_borrow",
    "きそく rule",
    "きびしい strict",
    "きぶん mood",
    "きめる to_decide_on",
    "きゅうしょく school_lunch",
    "きょういく education",
    "きょうかしょ textbook",
    "きょうみ interest",
    "きんじょ neighbourhood",
    "くださる to_give",
    "くらい dark",
    "グラス glass",
    "くれる to_give_(to_me/us)",
    "けが injury",
    "げき play/drama",
    "けっか result",
    "けっこん marriage",
    "けっこんしき wedding_ceremony",
    "けんがく study_visit",
    "こうりつ public",
    "こくご national_language",
    "こくりつ national",
    "こたえ answer",
    "こたえる to_answer",
    "ことば word",
    "このごろ recently",
    "これから from_now_on",
    "さいきん recently",
    "さいふ wallet",
    "さがす to_look_for",
    "さがる to_go_down",
    "さくぶん essay",
    "さしあげる to_give_[honorific]",
    "しかし however",
    "しけん examination",
    "しけん examination",
    "しつもん question",
    "しぬ to_die",
    "しばふ lawn",
    "しふく mufti",
    "じむしょ office",
    "しゅうがくりょこう school trip",
    "しゅうじ calligraphy",
    "じゆうじかん free_time",
    "じゅぎょう lesson",
    "じゅく cram_school",
    "じゅんび preparations",
    "しょくじ meal",
    "しょくどう dining_room",
    "しりつ private",
    "しんせつ） kind",
    "すぐ immediately",
    "すくない not_many",
    "ずっと all_the_time",
    "すてき wonderful",
    "すばらしい brilliant",
    "せいせき grade",
    "せいぶつ Biology",
    "せつめい explanation",
    "せんしゅ athlete",
    "そうしき funeral",
    "そつぎょう graduation",
    "そつぎょうしき graduation_ceremony",
    "たいいくさい sports_festival",
    "だいたい generally",
    "だから therefore",
    "だす to_put_out/to_send_(a_letter)",
    "ただしい correct",
    "たてもの building",
    "たとえば for_instance",
    "たのしみ to_look_forward_to",
    "たのしむ to_enjoy",
    "たのむ to_request",
    "たばこ cigarette",
    "すう to_smoke",
    "だんち housing_complex",
    "たんぼ rice_field",
    "チーム team",
    "ちゅうもん an_order",
    "ついている to_be_attached",
    "つける to_switch_on",
    "つたえる to_give_a_message",
    "つつむ to_wrap",
    "つれてくる to_accompany",
    "ていしょく set_menu",
    "でかける to_go_out",
    "できている to_be_made_of",
    "テクノロジー Technology",
    "てつだう to_assist",
    "でんき electricity",
    "でんしレンジ microwave_oven",
    "でんとうてき traditional",
    "どうやって how",
    "とおる to_go_through",
    "どくしょ reading",
    "とくべつ special",
    "トランプ cards",
    "なくなる to_pass_away",
    "なげる to_throw",
    "なま raw",
    "ならぶ to_line_up",
    "におい smell",
    "にる to_look_like",
    "にほんしき Japanese-style",
    "にゅうがく（する） to_start_school",
    "にゅうがくしき welcoming_ceremony_at_school",
    "にゅうがくしけん entrance_examination",
    "にんき popular",
    "ねだん price",
    "はじめて for_the_first_time",
    "はずかしい embarrassed",
    "はたけ field",
    "はらう to_pay",
    "ばんぐみ programme",
    "はんぶん half",
    "ヒーター heater",
    "ビール beer",
    "ひきわけ a_draw",
    "びっくり surprise",
    "ひるま daytime",
    "ふくしゅう revision",
    "ぶたにく pork",
    "ふつう normal",
    "ぶつり Physics",
    "ぶんか culture",
    "ぶんかさい cultural_festival",
    "ほか other",
    "ほとんど almost_all",
    "ほんとう true",
    "まける to_lose",
    "まもる to_preserve",
    "まわり around",
    "むすこ son",
    "むすめ daughter",
    "もちろん of_course",
    "もの thing",
    "もんだい problem_(in_test)",
    "やね roof",
    "やる to_do_(plain_language)",
    "ゆうえんち amusement_park",
    "ゆうがた evening",
    "ゆっくりする to_take_your_time",
    "ようしき western-style", 
    "ようしょく western-style_food_or_meal",
    "ようちえん kindergarten",
    "よびこう preparatory_school_for_university",
    "よろこぶ to_be_glad",
    "りゅうがく（を）する to_study_abroad",
    "りゅうがくせい overseas_student",
    "りょう hostel",
    "りょうしん parents",
    "れんが brick",
    "わかい young",
    "わしつ Japanese-style_room",
    "わらう to_laugh"]

# This list contains all of the NCEA level three words both japanese and english
LevelThreeWordList = [
    "アジア asia",
    "あつめる to_collect",
    "アルバイト casual_work", 
    "あんないする to_guide", 
    "あんないじょ information_bureau",
    "いそぐ to_hurry",
    "いちにちじゅう all_day_long",
    "いみ meaning",
    "ウール wool",
    "うけつけ reception",
    "うつくしい beautiful",
    "うんてんしゅ a_driver",
    "えいきょう influence",
    "えはがき post_card",
    "おうふく return_trip", 
    "おおい a_lot_of",
    "せわ care", 
    "おとしより old_person",
    "まつり festival",
    "おもいだす to_remember",
    "おもいで memories",
    "おんせん spa",
    "かいわ conversation",
    "かざん volcano",
    "ガソリン petrol",
    "ガソリンスタンド petrol_station",
    "かたみち one_way",
    "かなしい sad", 
    "かわる to_change",
    "かんがえ thought", 
    "かんがえる to_think", 
    "かんけい connection", 
    "かんこうきゃく tourist",
    "かんこうぎょう tourism",
    "かんこうち tourist_area",
    "かんじる to_feel",
    "きおん temperature",
    "きこう climate",
    "きせつ season",
    "きた north",
    "きって stamp",
    "きっと certainly",
    "きゅうりょう salary",
    "キリストきょう  Christianity",
    "くもる to_become_cloudy",
    "くらべる to_compare",
    "けいかん police_officer",
    "けいかく a_plan",
    "けいけん experience",
    "こうがい pollution",
    "こうぎょう  industry", 
    "こうこく advertisement", 
    "こうじょう  factory",
    "こうそくどうろ  motorway",
    "こうつう traffic", 
    "こうばん police_box",
    "こくさい  international",
    "こまる to_be_at_a_loss",
    "こわい scary", 
    "さいご the_very_last",
    "さいしょ the_very_first",
    "さか slope",
    "さびしい lonely", 
    "さんぎょう industry",
    "しげん resources",
    "しぜん nature", 
    "じつは actually",
    "しっぱい failure",
    "しつれい impolite",
    "じどうはんばいき vending_machine",
    "しま island",
    "しまぐに island_nation",
    "じむいん office_worker", 
    "しゅうかん weeks_duration",
    "しゅうきょう religion",
    "じゅうしょ address",
    "じゅうぶん enough", 
    "しゅっぱつ departure", 
    "しゅと capital_city",
    "しょうらい future",
    "しらべる to_check",
    "じんこう population",
    "しんじる to_believe",
    "しんとう Shinto",
    "ストレス stress",
    "すてる to_throw_out",
    "せいかつ life_style", 
    "ぜいかん customs",
    "ぜいきん tax",
    "せいじ politics",
    "せかい world",
    "せきにん responsibility",
    "そのまま as_is",
    "それで therefore",
    "たいし ambassador",
    "たいしかん embassy",
    "たいしょく retirement",
    "たいふう typhoon",
    "ただ free",
    "たてる to_build",
    "ためる to_save_up",
    "だんだん gradually",
    "ちか basement",
    "ちほう region",
    "ちゅうしん centre",
    "ちょうど  just",
    "つゆ rainy_season", 
    "ていねい polite", 
    "てきとう suitable",
    "できるだけ as_much_as_possible",
    "でぐち exit",
    "でんきせいひん electrical_appliances",
    "てんきよほう weather_forecast",
    "とうちゃく arrival",
    "とくに specially", 
    "ところで by_the_way",
    "とし city",
    "とちゅう on_the_way",
    "なくす to_lose_something",
    "にし west",
    "のうぎょう agriculture",
    "のりかえる to_change_trains",
    "ばいてん stall", 
    "はくぶつかん museum",
    "はってん development", 
    "はれる to_clear_up", 
    "はやし a_wood",
    "はんたい opposite", 
    "ひがし east",
    "ビザ Visa",
    "びじゅつかん art_gallery",
    "ひつよう necessary",
    "ふえる to increase_in_number",
    "ぶっきょう Buddhism",
    "へいや a_plain",
    "へいわ peace",
    "へんじ reply", 
    "ほう side", 
    "ぼうえき trade",
    "まじめ serious", 
    "まず first", 
    "まよう to_get_lost",
    "まんいん full", 
    "まんなか centre",
    "みずぎ swimwear",
    "みつける to_find",
    "みなと harbour", 
    "みなみ south",
    "むかし a_long_time_ago", 
    "むり unreasonable", 
    "めずらしい rare", 
    "もし if",
    "もっと more",
    "やくそく promise",
    "やちん the_rent",
    "よてい plan", 
    "よやく a_reservation", 
    "らく comfortable",
    "ラッシュアワー rush_hour",
    "わすれもの something_lost",
    ]



# This list contains all of the possible false answers
PossibleAnswers = [
    'receive',   
    'sales_counter',
    'to_be_glad',
    'greeting',
    'baby',
    'taste',
    'dangerous',
    'safety',
    'to_say',
    'busy',
    'diligently',
    'full',
    'entrance',
    'to_sit_an_exam',
    'sports_day',
    'air_conditioning',
    'pet_food',
    'to_choose',
    'to_support',
    'to_send',
    'uncooked_rice',
    'to_get_angry',
    'to_fall',
    'quiet',
    'the_same',
    'to_think',
    'parent',
    'hot_water',
    'to_swim',
    'foreign_country',
    'foreigner',
    'staircase',
    'Chemistry',
    'key',
    'umbrella',
    'housework',
    'to_lend',
    'to_tidy_up',
    'to_win',
    'school_term',
    'without_fail',
    'body',
    'to_borrow',
    'rule',
    'strict',
    'mood',
    'to_decide_on',
    'school_lunch',
    'education',
    'textbook',
    'textbook',
    'neighbourhood',
    'to_give',
    'dark',
    'glass',
    'to_give',
    'injury',
    'a_play',
    'result',
    'marriage',
    'wedding_ceremony',
    'study_visit',
    'public',
    'national_language',
    'national',
    'answer',
    'to_answer',
    'language',
    'recently',
    'from_now_on',
    'recently',
    'wallet',
    'to_look_for',
    'to_go_down',
    'essay',
    'to_give',
    'however',
    'exam',
    'question',
    'to_die',
    'the_lawn',
    'mufti',
    'office',
    'school_trip',
    'calligraphy',
    'free_time',
    'lesson',
    'cram_school',
    'preparations',
    'meal',
    'dining_room',
    'private',
    'kind',
    'immediately',
    'few',
    'much_more',
    'wonderful',
    'splendid',
    'results',
    'Biology',
    'explanation',
    'athlete',
    'funeral',
    'graduation',
    'graduation_ceremony',
    'sports_festival',
    'generally',
    'therefore',
    'to_put_out',
    'correct',
    'building',
    'for_instance',
    'to_enjoy',
    'to_ask',
    'cigarette',
    'smoke',
    'housing_estate',
    'rice_field',
    'team',
    'an_order',
    'to_be_attached',
    'to_turn_on',
    'to_give_a_message',
    'to_wrap',
    'to_accompany',
    'set_menu',
    'to_go_out',
    'to_be_made_of',
    'Technology',
    'to_help',
    'electricity',
    'microwave_oven',
    'tradition',
    'how_about',
    'to_go_through',
    'reading',
    'special',
    'cards',
    'to_pass_away',
    'to_throw',
    'raw',
    'to_line_up',
    'smell',
    'to_look_like',
    'japanese_style',
    'to_start_school',
    'welcoming_ceremony_at_school',
    'entrance_examination',
    'popular',
    'price',
    'for_the_first_time',
    'shy',
    'field',
    'to_pay',
    'programme',
    'half',
    'heater',
    'beer',
    'a_draw',
    'surprise',
    'daytime',
    'revision',
    'pork',
    'normal',
    'Physics',
    'culture',
    'cultural_festival',
    'other',
    'almost_all',
    'true',
    'to_lose',
    'to_obey',
    'around',
    'son',
    'daughter',
    'course',
    'thing',
    'problem',
    'roof',
    'amusement_park',
    'evening',
    'to_relax',
    'western_style',
    'western_style_meal',
    'kindergarten',
    'prep_school',
    'to_be_glad',
    'to_study_abroad',
    'overseas_student',
    'hostel',
    'parents',
    'brick',
    'young',
    'Japanese_style_room',
    'to_laugh',
    'asia',
    'to_collect',
    'casual_work',
    'to_guide',
    'information_bureau',
    'to_hurry',
    'all_day_long',
    'meaning',
    'wool',
    'reception',
    'beautiful',
    'a_driver',
    'influence',
    'post_card',
    'return_trip',
    'a_lot_of',
    'care',
    'old_person',
    'festival',
    'to_remember',
    'memories',
    'spa',
    'conversation',
    'volcano',
    'petrol',
    'petrol_station',
    'one_way',
    'sad',
    'to_change',
    'thought',
    'to_think',
    'connection',
    'tourist',
    'tourism',
    'tourist_area',
    'to_feel',
    'temperature',
    'climate',
    'season',
    'north',
    'stamp',
    'certainly',
    'salary',
    'Christianity',
    'to_become_cloudy',
    'to_compare',
    'police_officer',
    'a_plan',
    'experience',
    'pollution',
    'industry',
    'advertisement',
    'factory',
    'motorway',
    'traffic',
    'police_box',
    'international',
    'to_be_at_a_loss',
    'scary',
    'the_very_last',
    'the_very_first',
    'slope',
    'lonely',
    'industry',
    'resources',
    'nature',
    'actually',
    'failure',
    'impolite',
    'vending_machine',
    'island',
    'island_nation',
    'office_worker',
    'custom',
    'religion',
    'address',
    'enough',
    'departure',
    'capital_city',
    'future',
    'to_check',
    'population',
    'to_believe',
    'Shinto',
    'stress',
    'to_throw_out',
    'life_style',
    'customs',
    'tax',
    'politics',
    'world',
    'responsibility',
    'as_is',
    'therefore',
    'ambassador',
    'embassy',
    'retirement',
    'typhoon',
    'free',
    'to_build',
    'to_save_up',
    'gradually',
    'basement',
    'region',
    'centre',
    'just',
    'rainy_season',
    'polite',
    'suitable',
    'as_much_as_possible',
    'exit',
    'electrical_appliances',
    'weather_forecast',
    'arrival',
    'specially',
    'by_the_way',
    'city',
    'on_the_way',
    'to_lose_something',
    'west',
    'agriculture',
    'to_change_trains',
    'stall',
    'museum',
    'development',
    'to_clear_up',
    'a_wood',
    'opposite',
    'east',
    'Visa',
    'art_gallery',
    'necessary',
    'to',
    'Buddhism',
    'a_plain',
    'peace',
    'reply',
    'side',
    'trade',
    'serious',
    'first',
    'to_get_lost',
    'full',
    'centre',
    'swimwear',
    'to_find',
    'harbour',
    'south',
    'a_long_time_ago',
    'unreasonable',
    'rare',
    'if',
    'more',
    'promise',
    'the_rent',
    'plan',
    'a_reservation',
    'comfortable',
    'rush_hour',
    'something_lost',
    'ice_cream',
    'between',
    'to_meet',
    'blue',
    'red',
    'autumn',
    'to_open',
    'to_give/raise',
    'morning',
    'breakfast',
    'the_day_after_tomorrow',
    'foot/leg',
    'tomorrow',
    'over_there',
    'to_play',
    'head',
    'warm',
    'new',
    'hot',
    'after',
    'you',
    "(one's_own_)_older_brother",
    "(one's_own)_older_sister",
    'apartment',
    'not_much',
    'rain',
    'to_wash',
    'to_be_(inanimate)',
    'to_walk',
    'that_over_there',
    'good',
    'no',
    'house',
    'England',
    'to_go',
    'how_much_?',
    'together',
    'chair',
    'sore',
    'strawberry',
    'number_one',
    'when_?',
    'always',
    'cousin',
    'the_countryside',
    'dog',
    'now',
    'living_room',
    'younger_sister',
    'unpleasant',
    'to_be_(animate)',
    'to_put_inside',
    'colour',
    'various',
    'above',
    'cow',
    'behind',
    'song',
    'to_sing',
    'home',
    'horse',
    'sea',
    'to_sell',
    'noisy',
    'exercise',
    'drive',
    'picture',
    'movie',
    'movie_theatre',
    'English',
    'yes',
    'station',
    'pencil',
    'delicious',
    'doctor',
    'big',
    'Australia',
    'mother',
    'sweets',
    'money',
    'funny',
    'to_get_up',
    'customer',
    'to_be_late',
    'alcohol',
    'plate',
    'uncle',
    'grandfather',
    'slow',
    'green_tea',
    'change_(money)',
    'temple',
    'father',
    'younger_brother',
    'boy',
    'the_day_before_yesterday',
    'adult',
    'stomach',
    'name',
    'older_brother',
    'older_sister',
    'aunt',
    'grandmother',
    'chopsticks',
    'bath',
    'bath_room',
    'packed_lunch',
    'souvenir',
    'souvenir_shop',
    'heavy',
    'interesting',
    'to_get_off_(transport)',
    'end',
    'to_finish',
    'music',
    'girl',
    'company',
    'shopping',
    'to_buy',
    'to_return',
    'face',
    'to_take_(time/money)',
    'to_write',
    'student',
    'wind',
    'family',
    'good_looking',
    'school',
    'corner',
    'bag',
    'to_wear_(on_head)',
    'paper',
    'hair',
    'school_subject',
    'Tuesday',
    'light_(weight)',
    'garage',
    'curry_&_rice',
    'river',
    'cute',
    'Korea',
    'nurse',
    'easy',
    'try_hard',
    'tree',
    'Kiwifruit/kiwi',
    'yellow',
    'to_listen',
    'guitar',
    'dirty',
    'coffee_shop',
    'ticket',
    'yesterday',
    'kimono',
    'camp',
    'today',
    'church',
    'classroom',
    'siblings',
    'last_year',
    'dislike',
    'to_wear_(from_the_shoulder)',
    'beautiful',
    'bank',
    'Friday',
    'airport',
    'medicine',
    'chemist',
    'fruit',
    'mouth',
    'shoe',
    'shoe_shop',
    'socks',
    'cloudy',
    'about',
    'grounds',
    'class',
    'club_activities',
    'cricket',
    'Christmas',
    'to_come',
    'car',
    'black',
    'cellphone',
    'this_morning',
    'rubber',
    'Monday',
    'genkan',
    'healthy',
    'sightseeing',
    'park',
    'senior_high_school_student',
    'intersection',
    'school_principal',
    'senior_high_school',
    'tea',
    'coffee',
    'Coke',
    'here',
    'afternoon',
    'a.m.',
    'this_year',
    'child',
    'cooked_rice',
    'rubbish',
    'rubbish_bin',
    'to_be_crowded',
    'golf',
    'this',
    'about_(time)',
    'this_month',
    'concert',
    'this_week',
    'this_evening',
    'surfing',
    'fish',
    'fish_shop',
    'cherry_blossoms',
    'sashimi',
    'magazine',
    'soccer',
    'sugar',
    'cold',
    'salad',
    'sandwich',
    'walk',
    'competition',
    'examination',
    'introduction',
    'self_introduction',
    'job',
    'quiet',
    'under',
    'bicycle',
    'to_close',
    'society',
    'potato',
    'photograph',
    'shirt',
    'shower',
    'weekend',
    'homework',
    'housewife',
    'hobby',
    'primary_school_student',
    'primary_school',
    'skilful',
    'to_know',
    'white',
    'bullet_train',
    'traffic_lights',
    'bedroom',
    'shrine',
    'newspaper',
    'swimming',
    'watermelon',
    'Wednesday',
    'mathematics',
    'supermarket',
    'skirt',
    'like',
    'great',
    'a_little_bit',
    'cool',
    'steak',
    'Spain',
    'spoon',
    'sports',
    'trousers',
    'to',
    'slippers',
    'to_do',
    'to_sit',
    'tall',
    'short',
    'pupil',
    'uniform',
    'jersey',
    'narrow',
    'last_month',
    'last_week',
    'teacher',
    'never',
    'washing',
    'all',
    'cleaning',
    'there',
    'and',
    'outside',
    'nearby',
    'that',
    'and_then',
    'physical_education',
    'gymnasium',
    'university',
    'university_student',
    'all_right',
    'important',
    'usually',
    'kitchen',
    'a_burden',
    'tall',
    'a_lot',
    'only',
    'to_stand',
    'enjoyable',
    'food',
    'to_eat',
    'egg',
    'no_good',
    'who_?',
    'birthday',
    'small',
    'near',
    'subway',
    'map',
    '(my)_father',
    'brown',
    'bowl',
    'junior_high_school_student',
    'junior_high_school',
    'China',
    'a_bit',
    'geography',
    'to_use',
    'to_get_tired',
    'next',
    'to_arrive',
    'desk',
    'to_make',
    'boring',
    'strong',
    'fishing',
    'hand',
    'table',
    'letter',
    'to_be_able_to_do',
    'dessert',
    'department_store',
    'to_leave',
    'television',
    'weather',
    'train',
    'telephone',
    'Germany',
    'toilet',
    'how_?',
    'classmate',
    'animal',
    'zoo',
    'far_away',
    'toast',
    'sometimes',
    'good_at',
    'watch',
    'where_?',
    'place',
    'library',
    'cupboard',
    'very',
    'next_to',
    'to_stay',
    'friend',
    'Saturday',
    'drive',
    'bird',
    'to_take',
    'knife',
    'to_heal',
    'inside',
    'long',
    'summer',
    'what_?',
    'to_learn',
    'to',
    'not_good_at',
    'lively',
    'meat',
    "butcher's_shop",
    'Sunday',
    'Japan',
    'luggage',
    'New_Zealand',
    'garden',
    'to_take_off',
    'necktie',
    'cat',
    'netball',
    'sleepy',
    'to_lie_down',
    'farm',
    'exercise_book',
    'to_climb',
    'drink',
    'to_drink',
    'to_get_on',
    'tooth',
    'party',
    'yes',
    'motor_bike',
    'to_enter',
    'to_wear_(below_the_waist)',
    'box',
    'bridge',
    'to_run',
    'to_begin',
    'beginning',
    'bus_stop',
    'basketball',
    'computer',
    'to_work',
    'flower',
    'nose',
    'story/speech',
    'to_speak',
    '(my)_mother',
    'early/fast',
    'spring',
    'fine_weather',
    'volleyball',
    'number',
    'dinner',
    'hamburger',
    'to_play_(a_stringed_instrument)',
    'short',
    'picnic',
    'plane',
    'art',
    'left',
    'sheep',
    'person',
    'free_time',
    'hospital',
    'sick',
    'day_time',
    'building',
    'lunch',
    'wide',
    'pink',
    'pool',
    'fork',
    'to_put_on_weight',
    'pencil_case',
    'boat',
    'inconvenient',
    'winter',
    'blouse',
    'France',
    'old',
    'bad_at',
    'pet',
    'bed',
    'room',
    'strange',
    'study',
    'convenient',
    'hat',
    'home_room',
    'me_(for_males)',
    'want',
    'hockey',
    'white_board',
    'book',
    'book_shop',
    'bookcase',
    'every_morning',
    'every_week',
    'every_month',
    'every_year',
    'every_day',
    'every_evening',
    'before',
    'Maori',
    'to_turn',
    'awful_taste',
    'again',
    'town',
    'to_wait',
    'straight_ahead',
    'window',
    'comic',
    'large_apartment',
    'can_see',
    'mandarin',
    'right',
    'short',
    '水',
    'lake',
    'shop',
    'to_show',
    'street',
    'green',
    'ear',
    'everyone',
    'to_see',
    'milk',
    'difficult',
    'eye',
    'glasses',
    'menu',
    'Thursday',
    'To_take',
    'to_bring',
    'to_receive',
    'forest',
    'vegetable_shop',
    'baseball',
    'vegetable',
    'kind',
    'cheap',
    'a_break',
    'to_have_a_break',
    'to_lose_weight',
    'mountain',
    'mountain_climbing',
    'to_stop',
    'post_office',
    'famous',
    'snow',
    'clothes',
    'often',
    'beside',
    'to_read',
    'evening',
    'next_month',
    'next_week',
    'next_year',
    'rugby',
    'science',
    'cooking',
    'history',
    'restaurant',
    'practice',
    'rental_car',
    'to_understand',
    'to_forget',
    'me/I',
    'to_cross',
    'bad',
    'dress',]

#Words of the chosen level are moved into this list 
#words are processed out of this list and not one of the original lists because an intact copy of all the words needs to exist
#during the program words are deleted from the list
WordList = []

#when the player answers incorrectly the word is deleted from WordList and put into revision list 
revList = []


Level = 0        # The current level of vocab 
wordAmount = 0   # this is a holdover variable used when debuging the program, it does nothing functionaly
maxIndex = 0     #stores the current length of the word list, (used when picking a random word)
score = 0        #stores the players score
unprostring = "" #stores the current un-processed string from WordList
Word = []        #stores the the english word and the japanese word as two seperate items in a list.
MaxCounterVal = 0  # A debug variable that serves no functional prupose
CorrectWord = ""   #is the string with the current correct english word
ListLength = 0     # is the full length of the chosen levels vocab list (once asigned it's a static value) (used for the progress bar)
current = 0        #is the current progress value which determines the length of the progress bar
RevisionCompareVal = 0  #used to determine what revision word should be diplayed



#Order of variable storage:
#   WordList, RevList, Level, WordAmount, MaxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current




#the saving and loading of variables is done using pickle


#this is the saving function
def exit_handler():
   with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

#this triggers the save function at the closing of the program
atexit.register(exit_handler)

#A load function that can be called from anywhere
def FullLoad():
    with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

class MainMenu(Screen):
       
    title = ("日本語クイズ") #this is the text for the title screen  (Japanese Quiz)
    buttonOne = ("プレー")  #this is the text for the play button    (play)
    buttonTwo = ("出口")    #text for the quit button                 (exit)
    pass

#the vocab level menu
class GameMenuOne(Screen):   
    global Level
    global LevelOneWordList
    global LevelTwoWordList
    global LevelThreeWordList
    global WordList
    global ListLength

    Title = "どの語彙レベルですか？" #this is the text for the title screen  (What level do you want?)
    LevelOne = "レベル一"           # Level one button
    LevelTwo = "レベル二"           #Level two button
    LevelThree = "レベル三"         #Level three button
    Back = "返る"                   #Back button
    DisplayLevel = StringProperty()

    def onStart(self):
        global WordList 
        global revList 
        global Level
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal 
        global CorrectWord 
        global ListLength 
        global current 

        WordList = []
        revList = []
        Level = 0
        wordAmount = 0
        maxIndex = 0
        score = 0   
        unprostring = ""
        Word = ""
        MaxCounterVal = 0
        CorrectWord = ""
        ListLength = 0
        current = 0
    
    
    #these functions set up what level word list the player will be quized with
    # [DisplayLevel] is the string that shows the player their choice
    # [MaxIndex] is used as the max number for range od the random word chooser  (had to subtract by one to get the index right)
    def levelOne(self):
        global Level
        global WordList
        global LevelOneWordList
        global maxIndex
        global ListLength
        Level = 2
        WordList = LevelOneWordList
        ListLength = len(WordList)
        maxIndex = len(WordList) - 1
        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 
        self.DisplayLevel = "NCEA Level 2"
    def levelTwo(self):
        global Level
        global WordList
        global LevelTwoWordList
        global maxIndex
        global ListLength
        Level = 2
        WordList = LevelTwoWordList
        ListLength = len(WordList)
        maxIndex = len(WordList) - 1
        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 
        self.DisplayLevel = "NCEA Level 2"
    def levelThree(self):
        global Level
        global WordList
        global LevelThreeWordList
        global maxIndex
        global ListLength
        Level = 3
        WordList = LevelThreeWordList
        ListLength = len(WordList)
        maxIndex = len(WordList) - 1
        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 
        self.DisplayLevel = "NCEA Level 3"


    pass

#Continue/Start , Reset , revision menu
class SecondaryMenu(Screen):


    #Menu text
    ConStart = "スタート/続ける"  #Continue/Start
    Revis = "リビジョン"         # Revision
    Reset = "リセット"              #Reset
    Title = "何をしたいですか？"  #(Title text) What would you like to do?      
    Back = "返る"                  #Back

    #loads all of the global variables from the text file they're saved to
    def Load(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 

        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

    #sets all of the global variables to their default values and saves over any instance of them that already exists
    def ResetFunc(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        WordList = []
        revList = []
        Level = 0
        wordAmount = 0
        maxIndex = 0
        score = 0   
        unprostring = ""
        Word = ""
        MaxCounterVal = 0
        CorrectWord = ""
        ListLength = 0
        current = 0

        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

    #if there are already modified variables this function takes you to the game screen
    #if the variables are in their default states it sends you to the level selection menu
    def ConStartFunc(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        global WordList

        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

        if Level == 0:
            self.ResetFunc()
            self.manager.current = "GameMenuOne"

        if Level != 0:
            with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 
            self.manager.current = "Game"
    
    pass

#the main game loop
class Game(Screen):
    

    JapaneseWord = StringProperty()
    EnglishWord = StringProperty()
    englishanswer = ObjectProperty()
    TitleString = StringProperty()
    InputTextThing = StringProperty()
    AnswerOne = StringProperty()
    AnswerTwo = StringProperty()
    AnswerThree = StringProperty()
    AnswerFour = StringProperty()

    

    Back = "返る" #back 

    OtherCounterVal = 0 #debug
    
    Score = StringProperty() #Makes ScoreVal work with kivy
   
    #on start an unprocessed word is taken from WordList and is split inot its japanese display word and its correct english answer.
    def Start(self):
        global wordAmount
        global WordList
        global revLists
        global maxIndex
        global unprostring
        global Word
        global score
        global current
        global CorrectWord
        global Level 
        global MaxCounterVal
        global ListLength 
        global PossibleAnswers

        #load in the saved global variables
        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)
        


        self.Score = str(score)
        self.ids.my_progress_bar.value = current
        
        #if Start() is called and there are no more words left in the list it sends you to the end screen
        if len(WordList) == 1:
            print("wags")
            self.manager.current = "EndScreen"
        

        #max index is used to set the upper value of the random range used to pick the random word
        maxIndex = len(WordList) - 1

        #if Start() is called and there are no more words left in the list it sends you to the end screen
        if maxIndex == -1:
            self.manager.current = "EndScreen"

        #debug lines
        print(str(maxIndex))
        print(len(WordList))
        print(WordList)

        #picks a random word from the word list 
        unprostring = WordList[random.randint(0, maxIndex)]
        
        #splits the word into two items in a list (japanese - english)
        Word = unprostring.split()

        #defines an empty list where the correct and incorrect answers will be added to
        AnswerList = []
        AnswerList.append(Word[1]) #adds correct answer
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        random.shuffle(AnswerList) #shuffles the list so correct and incorrect answers are in random order

        self.JapaneseWord = Word[0] #sets the "display word" as the japanese of the random word chosen above
        CorrectWord = Word[1] #sets the "answer word" as the english of the random word chosen above

        self.AnswerOne = AnswerList[0].replace("_", " ") #replaces underscores in the answer with spaces
        self.AnswerTwo = AnswerList[1].replace("_", " ") #replaces underscores in the answer with spaces
        self.AnswerThree = AnswerList[2].replace("_", " ") #replaces underscores in the answer with spaces
        self.AnswerFour = AnswerList[3].replace("_", " ") #replaces underscores in the answer with spaces

        
        #if self.AnswerOne.replace(" ", "_") == Word[1]:
            #CorrectId = "One"

        #if self.AnswerTwo.replace(" ", "_") == Word[1]:
            #CorrectId = "Two"

        #if self.AnswerThree.replace(" ", "_") == Word[1]:
            #CorrectId = "Three"

        #if self.AnswerFour.replace(" ", "_") == Word[1]:
            #CorrectId = "Four"
    


    def ProgressUpdate(self):
        global WordList
        global ListLength
        global current

        #gets the current progress value 
        current = self.ids.my_progress_bar.value

        #defines the maximum progress value as one 
        if current == 1:
            current = 0

        #adds on increment to the progress value 
        current += (1/int(ListLength))

        #updates the progress bar with the current progress value
        self.ids.my_progress_bar.value = current

        #saves the new variables
        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

    #is called whenever an answer button is clicked
    def Submit(self, instance):
        global score
        global streak
        global WordList
        global wordAmount
        global Word
        global MaxCounterVal
        global AttemptCounter
        global revList
        global unprostring
        global AttemptCounter
        global CorrectWord
        global ColourOne
        
        #gets the text of the pressed button
        PressedButton = instance.text

        #if the text of the pressed button (with underscores instead of spaces) is equal to the CorrectWord then it adds one to score,
        #removes the unprocessed version of the word from the list, saves the new variables to the text file and sends you to the correct screen
        if PressedButton.replace(" ", "_") == CorrectWord:
            WordList.remove(unprostring)
            score += 1
            self.Score = str(score)
            self.manager.current = "CorrectScreen"
            with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

            
        #if the text of the pressed button (with underscores instead of spaces) is not equal to the CorrectWord then it removes the uprocessed word from the list and adds it to the revision list, its saves the variaables ot the text file and send you to the incorrect screen  
        if PressedButton.replace(" ", "_") != CorrectWord:
            WordList.remove(unprostring)
            revList.append(unprostring)
            self.manager.current = "InCorrectScreen"
            with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

           
            
    

    
    

    pass

#these screen are to show whether or not you got answer correct or not
class CorrectScreen(Screen):

    def Skip(self):
        time.sleep(0.3)
        self.manager.current = "Game"
        #after 0.3 second you are sent back to the main game loop
        

    pass 

#these screen are to show whether or not you got answer correct or not
class InCorrectScreen(Screen):

    def Skip(self):
        time.sleep(0.3)
        self.manager.current = "Game"
        #after 0.3 second you are sent back to the main game loop

    pass

#when all of the words have been removed from the list you are sent to this screen
class EndScreen(Screen):
    

    ScoreVal = StringProperty() #makes ScoreVal word with kivy

    #title texts
    Back = "返る"                 #Back
    Revis = "リビジョン"          #revision

    #called when you enter the screen
    def Start(self):
        global current
        global score

        #gets the current progres bar level
        self.ids.my_progress_bar.value = current

        #gets the current score
        self.ScoreVal = str(score)
        


    
    
    pass

#a screen where you can look through all of the words on your revision list
class RevisionList(Screen):

    #makes the values work with kivy
    CurrentEnglishWord = StringProperty()
    CurrentJapaneseWord = StringProperty()

    Back = "返る" #Back
    
    #called on entry to the program
    def Start(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        global revList
        global RevisionCompareVal

        #gets the saved variables
        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

        try:
            #gets the word in the revision list with the index value equal to RevisionCompareVal and splits it and makes a list out of the two items
            CurrentUnproWord = revList[RevisionCompareVal].split()

            self.CurrentJapaneseWord = CurrentUnproWord[0] #sets the japanese display word equal to the japanese item in the list
            self.CurrentEnglishWord = CurrentUnproWord[1].replace("_", " ") #sets the english display word equal to the english item in the list
        
        except:
            #sets the display words to be blank
            self.CurrentJapaneseWord = ""
            self.CurrentEnglishWord = ""

        
    #called when the next word button is pressed
    def NextWord(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        global revList
        global RevisionCompareVal

        #updates the variables
        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

        #if you haven't reached the end of the revision list it adds one to the revisioncompareval and calls the start function updating the display
        if RevisionCompareVal < (len(revList)-1):
            RevisionCompareVal += 1
            self.Start()

        #if you have reached the end of the revision list it calls the start function again without changing the variables meaning the displayed words will be the same
        else:
            self.Start()

    #called when the previuos word button has been pressed
    def LastWord(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        global revList
        global RevisionCompareVal

        #updates the variables
        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

        #if you haven't reached the end of the revision list it subtracts one to the revisioncompareval and calls the start function updating the display
        if RevisionCompareVal > 0:
            RevisionCompareVal -= 1
            self.Start()

        else: 
            #if you have reached the start of the revision list it calls the start function again without changing the variables meaning the displayed words will be the same
            self.Start()



    pass

#sorts all of the screens
class WindowManager(ScreenManager):
    pass

#defines the .kv file to run with what encoding to use
kv = Builder.load_file("GUICode4.1.kv" , encoding='utf-16')

#the main app class
class NCEAJapaneseQuizApp(App):
    
    #builds the app 
    def build(self):
       return kv


#runs the built app
NCEAJapaneseQuizApp().run()
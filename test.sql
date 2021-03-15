-- --------------------------------------------------------
-- ホスト:                          127.0.0.1
-- サーバーのバージョン:                   8.0.12 - MySQL Community Server - GPL
-- サーバー OS:                      Win64
-- HeidiSQL バージョン:               11.1.0.6116
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- mydb のデータベース構造をダンプしています
CREATE DATABASE IF NOT EXISTS `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `mydb`;

--  テーブル mydb.reaction の構造をダンプしています
CREATE TABLE IF NOT EXISTS `reaction` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `site` varchar(50) DEFAULT '',
  `smarts` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `condition` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- テーブル mydb.reaction: ~35 rows (約) のデータをダンプしています
DELETE FROM `reaction`;
/*!40000 ALTER TABLE `reaction` DISABLE KEYS */;
INSERT INTO `reaction` (`id`, `name`, `site`, `smarts`, `condition`) VALUES
	(1, 'アルコールの脱水反応', 'C=C', '[C:1]=[C:2] >> [C:1][C:2]-O', 'アルコールから二重結合を得る反応。濃硫酸を加えて加熱するといった操作でH2Oを脱離させる。'),
	(2, 'ハロゲン化アルキルの脱離反応', 'C=C', '[C:1]=[C:2] >> [C:1][C:2]Cl', 'ハロゲン置換基から二重結合を得る反応。塩基を加えるなどの操作でハロゲン原子と水素原子1つを脱離させる。'),
	(3, 'フィッシャーエステル合成反応', 'CC(=O)OC', '[C:1][C:2](=[O:3])[O:4][C:5] >> [C:1][C:2](=[O:3])O.[O:4][C:5]', '酸触媒を用いた基本的なエステル縮合反応。可逆反応であるため、アルコールを過剰量加える、濃硫酸で脱水するといった手法で平衡を偏らせる必要がある。'),
	(4, 'マンニッヒ反応', 'NCCC=O', '[N:1][C:2][C:3][C:4]=[O:5] >> [N:1].[C:2]=O.[C:3][C:4]=[O:5]', '第二級アミン、アルデヒド、ケトンによる三成分縮合反応。酸性条件下で反応させる。'),
	(5, 'パール・クノール ピロール合成', 'c1cccn1C', '[c:1]1[c:2][c:3][c:4][n:5]1[C:6] >> [C:1](=O)[C:2][C:3][C:4]=O.[N:5][C:6]', '1,4ジケトンと第一級アミンを縮合させてピロールを形成する反応。酸性条件にて進行させる脱水反応である。'),
	(6, 'パール・クノール フラン合成', 'c1ccco1', '[c:1]1[c:2][c:3][c:4][o:5]1 >> [C:1](=O)[C:2][C:3][C:4]=[O:5]', '1,4ジケトンを分子内縮合させてフランを形成する反応。酸性条件にて進行させる脱水反応である。'),
	(7, 'パール・クノール チオフェン合成', 'c1cccs1', '[c:1]1[c:2][c:3][c:4][s:5]1 >> [C:1](=O)[C:2][C:3][C:4]=O', '1,4ジケトンをもとにしてチオフェンを生成する反応。はじめにローソン試薬などの硫化剤を添加してジケトンのカルボニル酸素を硫黄に置換する。置換後の分子は有毒の硫化水素を発生させながら分子内縮合を進行し、チオフェンとなる。'),
	(8, '芳香族求電子置換反応', 'c1ccccc1Br', '[c:1]1[c:2][c:3][c:4][c:5][c:6]1[Br:7] >> [c:1]1[c:2][c:3][c:4][c:5][c:6]1.Br[Br:7]', 'FeBr3などのルイス酸触媒を用いるベンゼンへの置換反応。電子供与基や電子吸引基の存在によって付加する位置が変わってくるので注意する。'),
	(9, '芳香族求電子置換反応', 'c1ccccc1Cl', '[c:1]1[c:2][c:3][c:4][c:5][c:6]1[Cl:7] >> [c:1]1[c:2][c:3][c:4][c:5][c:6]1.Cl[Cl:7]', 'FeCl3などのルイス酸触媒を用いるベンゼンへの置換反応。電子供与基や電子吸引基の存在によって付加する位置が変わってくるので注意する。'),
	(10, '芳香族求電子置換反応', 'c1ccccc1[N+](=O)[O-]', '[c:1]1[c:2][c:3][c:4][c:5][c:6]1[N+:7](=[O:8])[O-:9] >> [c:1]1[c:2][c:3][c:4][c:5][c:6]1.[N+:7](=[O:8])(O)[O-:9].OS(=O)(=O)O', 'ベンゼンにニトロ基を付与する置換反応。硝酸と硫酸を混合することで生じる[NO2]+がベンゼンと求電子置換反応を起こす。位置選択性に注意。'),
	(11, '芳香族求電子置換反応', 'c1ccccc1S(=O)(=O)O', '[c:1]1[c:2][c:3][c:4][c:5][c:6]1[S:7](=[O:8])(=[O-:9])[O:10] >> [c:1]1[c:2][c:3][c:4][c:5][c:6]1.[S:7](=[O:8])([=O:9])=[O:10].OS(=O)(=O)O', 'ベンゼンにスルホン基を付与する置換反応。硝酸と三酸化硫黄を加えて反応を進行させる。ちなみに可逆反応である。'),
	(12, 'フリーデル・クラフツ アルキル化反応', 'c1ccccc1C', '[c:1]1[c:2][c:3][c:4][c:5][c:6]1[C:7] >> [c:1]1[c:2][c:3][c:4][c:5][c:6]1.[C:7]Cl', 'ベンゼンをアルキル化する置換反応。触媒にAlCl3などルイス酸を用いて炭素鎖のカルボカチオンを生成する。塩素は臭素など他ハロゲンでも可。過剰反応や転移に注意。'),
	(13, 'アルドール反応', 'C=CC=O', '[C:1]=[C:2][C:3]=[O:4] >> [C:1]=O.[C:2][C:3]=[O:4]', '炭素-炭素二重結合を形成する代表的な反応。はじめに酸または塩基触媒を用いて求核付加を進行させ、その後に生じたヒドロキシ基から脱水反応を用いて二重結合を作る。'),
	(14, 'アセト酢酸エステル合成', 'C(=O)[C*H2]C', '[C:1](=[O:2])[C:3]([H:4])[C:5] >> [C:1](=[O:2])[C:3]([H:4])C(=O)OC.[C:5]I', 'アセト酢酸エステルを利用して置換ケトンを得る反応。アセト酢酸エステルは脱プロトンしやすく、塩基を加えればハロゲン化アルキルで置換できる。その後エステルをNaOHで切断し、CO2を取り除けば置換ケトンが得られる。'),
	(15, 'アセト酢酸エステル合成(2置換)', 'C(=O)C(C)C', '[C:1](=[O:2])[C:3]([C:4])[C:5] >> [C:1](=[O:2])[C:3]C(=O)OC.[C:4]I.[C:5]I', 'アセト酢酸エステルを利用して置換ケトンを得る反応。アセト酢酸エステルは脱プロトンしやすく、塩基を加えればハロゲン化アルキルで置換できる。この置換を2回行い、その後エステルをNaOHで切断し、CO2を取り除けば2置換ケトンが得られる。'),
	(16, 'ヘンリー反応', 'C(O)C[N+](=O)[O-]', '[C:1]([O:2])[C:3][N+:4](=[O:5])[O-:6] >> [C:1](=[O:2])H.[C:3][N+:4](=[O:5])[O-:6]', 'ニトロアルカンを用いたアルドール反応の一種。弱い塩基を用いて反応を進行させる。触媒を用いて立体選択性を管理する。'),
	(17, 'ロビンソン環化', 'C1CC(=O)C=CC1', '[C:1]1[C:2][C:3](=[O:4])[C:5]=[C:6][C:7]1 >> [C:1]=[C:2][C:3](=[C:4])[C:5].[C:7][C:6]=O', '6員環を形成する縮合反応。塩基を加えると最初にマイケル付加が進行し、その後に分子内アルドール縮合が起きて6員環を形成する。前駆体のカルボニル化合物がマイケル付加に適しているか注意。'),
	(18, '還元的アミノ化', 'CCN', '[C:1][C:2][N:3] >> [C:1][C:2]=O.[N:3]', 'アミンを生成する反応。ヒドリド還元剤を用いて反応を進行させる。ヒドリド還元剤にNaBH3CNを用いるものはボーチ還元と呼ばれ代表される。'),
	(19, 'ストレッカーアミノ酸合成', 'C(N)C(=O)O', '[C:1]([N:2])[C:3](=[O:4])[O:5] >> [C1:]=O.Na[C:3]#N.[N:2]', '三成分縮合によるアミノ酸の合成法。最初にアルデヒドをアンモニアで置換してイミンを生成し、次にシアン化水素を付加する。最後にシアノ基を加水分解することでアミノ酸が得られる。'),
	(20, 'ハンチュ ピロール合成', 'c1c(C(=O)O)ccn1', '[c:1]1[c:2]([C:6](=[O:7])[O:8])[c:3][c:4][n:5]1 >> [C:1](=O)[C:2][C:6](=[O:7])[O:8].Cl[C:3][C:4]=O.[N:5]', '三成分反応によるピロールの合成法。最初にケトンにアンモニアを加えたのち、ハロゲン化ケトンを加えることでC-C結合が形成される。その後分子内縮合が進行してピロールが得られる。'),
	(21, 'フェイスト・ベナリー フラン合成', 'c1c(C(=O)O)cco1', '[c:1]1[c:2]([C:6](=[O:7])[O:8])[c:3][c:4][o:5]1 >> [C:1](=O)[C:2][C:6](=[O:7])[O:8].Cl[C:3][C:4]=O', '二成分反応によるフランの合成法。最初にケトンに塩基を加えたのち、ハロゲン化ケトンを加えることでアルドール反応が進行し、その後分子内脱水反応によってフランが得られる。'),
	(22, 'ピナコール転移', 'CC(=O)C(C)(C)C', '[C:1][C:2](=[O:3])[C:4]([C:6])([C:7])[C:5] >> [C:1][C:2]([C:5])([O:3])[C:4](O)([C:6])[C:7]', '転移反応を伴いながらカルボニル化合物を得る反応。環拡大などが可能な有用反応。2つのヒドロキシ基を持つピナコールは強酸性条件で転移しながら脱水反応を起こす。置換基は電子豊富であるものが転移しやすいが、様々な転移の可能性が生じることに注意。'),
	(23, 'セミピナコール転移', 'CC(=O)C(C)(C)C', '[C:1][C:2](=[O:3])[C:4]([C:6])([C:7])[C:5] >> [C:1][C:2]([C:5])([O:3])[C:4](Cl)([C:6])[C:7]', '転移反応を伴いながらカルボニル化合物を得る反応。ピナコール反応の派生形で、脱離基にハロゲンやアルコール誘導体などを用いることで転移の方向を制御できるようになった。酸性条件などで脱離基を活性化させることで反応が進行する。転移は電子豊富な置換基が優先される。'),
	(24, 'ベックマン転移', 'C(=O)NC', '[C:1](=[O:2])[N:3][C:4] >> [C:1](=[N:3]O)[C:4]', 'オキシム(C=N-OH)からアミドを得る反応。酸触媒を加えるとH2Oが脱離し転移が進行してC-N=Cの構造となる。その後に加水分解を行うことでアミドが得られる。'),
	(25, 'バイヤー・ビリガー酸化', 'C(=O)OC', '[C:1](=[O:2])[O:3][C:4] >> [C:1](=[O:2])[C:4]', 'ケトンから転移によってエステルを得る反応。主にmCPBAという過酸を用いて反応を進行させる。非対称ケトンが反応する場合、級数が高いアルキル基が優先して酸素上に転移することに注意。'),
	(26, 'ベンジル酸転移', 'CC(O)C(=O)O', '[C:6][C:1]([O:2])[C:3](=[O:4])[O:5] >> [C:1](=[O:2])[C:3](=[O:4])[C:6]', '転移によってα-ヒドロキシカルボン酸を得る反応。ジケトンに塩基を作用させることで反応が進行する。環縮小などに用いられる反応である。α-ジケトンのα位にプロトンが存在する場合、副反応によって収率が低くなる。'),
	(27, 'ウォルフ転移', 'CC=C=O', '[C:1][C:2]=[C:3]=[O:4] >> [C:1][C:3](=[O:4])[C:2]=[N+]=[N-]', 'ジアゾケトンから転移を伴ってケテンを得る反応。ジアゾケトンは加熱や光照射、銀触媒によって脱窒素化され、カルベン中間体が生じる。カルベンがカルボニル炭素に攻撃して転移が起こり、ケテンが得られる。'),
	(28, 'ケテンの付加反応', 'CC(=O)O', '[C:1][C:2](=[O:3])[O:4] >> [C:1]=[C:2]=[O:3].[O:4]', 'ケテンからエステルやカルボン酸を得る反応。ケテンは不安定で反応性が高く、主にウォルフ転移などを用いて生成する。'),
	(29, 'クルチウス転移', 'CN', '[C:1][N:2] >> [C:1]C(=O)O.c1ccccc1OP(=O)(Oc2ccccc2)[N:2]=[N+]=[N-].O', 'カルボン酸からアミンを得る反応。カルボン酸にジフェニルリン酸アジドを混合して加熱すると、酸アジドを経て転移が起こりイソシアネート(-N=C=O)が生成される。これはH2Oによって加水分解されアミンとなる。アミンの立体化学は保持される点が優秀。'),
	(30, 'アッペル反応', 'CBr', '[C:1][Br:2] >> [C:1]O.[Br:2]C(Br)(Br)Br', '第一級、二級アルコールからハロゲン化合物を得る反応。アルコールと四ブロモ化炭素をトリフェニルホスフィン(PPh3)と共に混合することで反応が進行する。中性条件にて反応を行う。'),
	(31, 'アッペル反応', 'CCl', '[C:1][Cl:2] >> [C:1]O.[Cl:2]C(Cl)(Cl)Cl', '第一級、二級アルコールからハロゲン化合物を得る反応。アルコールと四クロロ化炭素をトリフェニルホスフィン(PPh3)と共に混合することで反応が進行する。中性条件にて反応を行う。'),
	(32, 'アッペル反応', 'CI', '[C:1][I:2] >> [C:1]O.[I:2]I', '第一級、二級アルコールからハロゲン化アルキルを得る反応。アルコールとヨウ素をトリフェニルホスフィン(PPh3)と共に混合することで反応が進行する。中性条件にて反応を行う。'),
	(33, 'ウィッティヒ反応', 'C=C', '[C:1]=[C:2] >> [C:1]=O.c1ccccc1P(c2ccccc2)(c3ccccc3)=[C:2]', 'リンイリドとカルボニルからC=C結合を得る反応。前駆体のリンイリドはウィッティヒ試薬と呼ばれる。リンイリドが電子吸引性置換基を持つ安定イリドである場合はE体、そうでない不安定イリドの場合はZ体を生成するという選択性を持つ。'),
	(34, 'ウィッティヒ試薬の合成', 'c1ccccc1P(c2ccccc2)(c3ccccc3)=[C:1]', 'c1ccccc1P(c2ccccc2)(c3ccccc3)=[C:1] >> c1ccccc1P(c2ccccc2)(c3ccccc3).[C:1]Br', 'ウィッティヒ反応に用いるリンイリド(ウィッティヒ試薬)を得る反応。ハロゲン化アルキルとトリフェニルホスフィンを反応させたのち、塩基でプロトンを取り除くとウィッティヒ試薬が生成される。'),
	(35, 'アルコールのアセチル化', 'COC(=O)C', '[C:1][O:2][C:3](=[O:4])[C:5] >> [C:1][O:2].CC(=O)O[C:3](=[O:4])[C:5]', 'ヒドロキシ基をアセチル基に変換する反応。ヒドロキシ基の酸素電子が無水酢酸のカルボニル炭素を攻撃することで反応が進行する。不可逆反応であり副生成物も酢酸という取り扱いやすい反応である。'),
	(36, 'フェノールのアセチル化', 'cOC(=O)C', '[c:1][O:2][C:3](=[O:4])[C:5] >> [c:1][O:2].CC(=O)O[C:3](=[O:4])[C:5]', 'ヒドロキシ基をアセチル基に変換する反応。ヒドロキシ基の酸素電子が無水酢酸のカルボニル炭素を攻撃することで反応が進行する。不可逆反応であり副生成物も酢酸という取り扱いやすい反応である。'),
	(37, 'フィッシャーエステル合成反応', 'CC(=O)Oc', '[C:1][C:2](=[O:3])[O:4][c:5] >> [C:1][C:2](=[O:3])O.[O:4][c:5]', '酸触媒を用いた基本的なエステル縮合反応。可逆反応であるため、アルコールを過剰量加える、濃硫酸で脱水するといった手法で平衡を偏らせる必要がある。'),
	(38, 'フィッシャーエステル合成反応', 'cC(=O)OC', '[c:1][C:2](=[O:3])[O:4][c:5] >> [c:1][C:2](=[O:3])O.[O:4][c:5]', '酸触媒を用いた基本的なエステル縮合反応。可逆反応であるため、アルコールを過剰量加える、濃硫酸で脱水するといった手法で平衡を偏らせる必要がある。');
/*!40000 ALTER TABLE `reaction` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

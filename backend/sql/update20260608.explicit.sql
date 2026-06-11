-- 2026-06-08 test25 -> test26 导师资料逐条回写脚本
-- 目标：
-- 1. 仅将 test25 中导师账号的介绍 / 手机 / 邮箱，逐条更新到 test26。
-- 2. 每个用户名单独执行 UPDATE，WHERE 条件就是 username。
-- 3. 不做 INSERT / DELETE / TRUNCATE / 重建表操作。
-- 4. 仅同步 role_code = advisor 的账号。
-- 5. 仅写入源库里非空的介绍 / 手机 / 邮箱。
-- 6. 执行前请确认目标库为 test26。

BEGIN;

UPDATE dtlms_user_profiles SET introduction = '乔宇，从事计算机视觉、模式识别、深度学习、基础模型、具身智能、Infra等方面的研究，近期聚焦原生多模态大模型、世界模型、算力数据基础设施等。领导研发了国内首个广泛覆盖多种视觉任务的通用视觉大模型，以及开源社区性能领先的多模态大模型书生·万象InternVL系列。论文发表300余篇，累计被引12万余次，H指数150+，获得发明专利授权100余项。获得王选杰出青年学者奖、CVPR 2023最佳论文奖，AAAI 2021杰出论文奖、ACL 2024杰出论文奖等，以第一完成人获广东省技术发明一等奖。入选国家级领军人才计划、科技部中青年科技创新领军人才、上海市优秀学术带头人、中科院百人计划等。
邮箱：qiaoyu@pjlab.org.cn （请务必同时抄送至 denghuipeng@pjlab.org.cn）', phone_number = '13590305261', email = 'qiaoyu@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'qiaoyu';
UPDATE dtlms_users SET phone_number = '13590305261', email = 'qiaoyu@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'qiaoyu' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '何军军，上海人工智能实验室青年科学家。目前主要研究方向为多模态理解、多模态生成、多模态生成理解一体化，以及多智能体及其在医学领域的应用。谷歌学术引用1.1万余次，H指数46，入选斯坦福大学全球前2%顶尖科学家榜单，荣获2025 MICCAI Best Paper and Young Scientist Awards Shortlist和MICCAI 2025 Best Workshop Paper Award。在国际挑战赛中获得10余项奖项，其中6项冠军。担任上海人工智能实验室通用医疗GMAI团队负责人，带领团队在医疗AI领域构建并开源了多个大规模基准数据集和高性能模型。代表性成果包括：3D医学影像预训练模型STU-Net，医学影像分割基础模型SAM-Med2D和SAM-Med3D，大规模系统化医学多模态评测基准OmniMedVQA与GMAI-MMBench，通用医疗多模态大模型GMAI-VL，超大分辨率病理WSI多模态大模型SlideChat，以及大规模眼底彩照生成模型RetinaLogos和眼科手术视频生成模型Ophora等。近期，团队开源项目Project Imaging-X（大规模医学影像数据综述与开源开放共享平台）在国内外引起广泛关注。此外，还参与了通用多模态大模型InternVL、科学多模态大模型Intern-S1，以及生成理解一体化模型Lumina-Dimoo等重要项目的研发工作。', phone_number = '13388899999', email = 'hejunjun@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'hejunjun';
UPDATE dtlms_users SET phone_number = '13388899999', email = 'hejunjun@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'hejunjun' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = 'https://conghui.ai/
at the Shanghai AI Laboratory, I founded the OpenDataLab team to break through this barrier. We developed MinerU , which transforms unstructured documents into high-quality data that large models can learn from. Within a year of release, MinerU earned 50,000 GitHub stars with over 1 billion API calls, and is used in production by Google, Huawei, Alibaba, and over 100 other enterprises. Our team also curates high-quality datasets for leading models such as InternLM and InternVL.
I have authored over 200 papers in top-tier venues, garnered 18449 citations on Google Scholar, and received honors including the Gordon Bell Prize, an ACL Best Theme Paper Award, and the WAIC Yunfan Award. I’m not just doing research — I’m building the data infrastructure for the AI era.
We are hiring! I am actively seeking talented Ph.D. students, postdoctoral fellows, interns, and full-time researchers. If you are passionate about building the future of AI, I welcome you to contact me via email.
EMAIL：heconghui@pjlab.org.cn', email = 'heconghui@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'heconghui';
UPDATE dtlms_users SET email = 'heconghui@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'heconghui' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '刘翼豪博士现任上海人工智能实验室青年科学家，正带领团队探索下一代多模态基础模型的新架构。团队希望让 AI 不再只是“看得懂”或“画得好”，而是能够在统一框架中完成“理解—生成—推理—评价”的闭环，让模型具备更强的综合智能与自我改进能力。目前，团队重点关注全离散扩散多模态统一模型、面向科学内容与知识驱动的因果一致建模、多模态后训练及奖励对齐等方向，致力于为下一代通专融合基础模型和科学智能应用探索新的技术路线。简单来说，就是希望让模型既能生成图像、编辑图像、理解视觉内容，也能参与科学图文生成、多模态推理和复杂知识表达。近年来，带领团队研发了全离散扩散多模态统一模型 Lumina-DiMOO、专家级美学理解大模型 ArtiMuse、统一感知层级图像理解模型 UniPercept 等代表性工作，并持续推进图像视频增强（LinearSR、DiffVSR、Lumina-OmniLV）、物理真实图像编辑评测（PICABench）、气象生成理解统一模型（Omni-Weather）等系列研究。曾获中国科学院院长奖、朱李月华优秀博士生奖、中科院深圳先进院院长创新奖、CVMJ 2025 最佳论文提名奖等荣誉，并在 PIRM 2018 感知超分辨、AIM 2020 视频插帧、NTIRE 2021 HDR 增强、UDC 2020 屏下相机复原等国际视觉竞赛中取得冠军、亚军和季军等成绩。谷歌学术总引用1万余次，h-index：26。
个人主页链接：https://lyh-18.github.io/
邮箱地址：liuyihao@pjlab.org.cn', email = 'liuyihao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'liuyihao';
UPDATE dtlms_users SET email = 'liuyihao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'liuyihao' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '吕照阳博士现任上海人工智能实验室青年科学家，研究方向为三维资产生成与具身仿真数据合成。此前负责了Simulation Ready三维物体资产生成与InternDataEngine具身仿真引擎的开源与发布。其中，Infinite Mobility实现了秒级无限生成高质量可交互物体，生成成本降至传统人工标注方法的百分之一，在95%以上的用户评测中关节质量达到或超过传统数据集水平，已应用于桃源2.0、Isaac Sim等主流仿真平台；MeshCoder 首创以大语言模型驱动点云到可编辑结构化代码的生成范式，在重建精度上较传统方法实现数量级领先；InternDataEngine打通了自动化数据合成流水线，8卡4090单日数据产能达数百小时，验证大规模合成数据可作为VLA预训练的重要资源。吕照阳博士在顶级学术会议和期刊上共发表近20篇论文，谷歌学术引用超过 2300，h-index 为15。
邮箱 lvzhaoyang@pjlab.org.cn
谷歌学术 https://scholar.google.com/citations?user=gkXFhbwAAAAJ&hl=en
代表性工作 https://infinite-mobility.github.io/，https://daibingquan.github.io/MeshCoder/，https://code-as-room.github.io/', email = 'lvzhaoyang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'lvzhaoyang';
UPDATE dtlms_users SET email = 'lvzhaoyang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'lvzhaoyang' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET email = 'wujiang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wujiang';
UPDATE dtlms_users SET email = 'wujiang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wujiang' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '吴郦军，长期从事人工智能与大模型方向研究，聚焦数据智能、推理模型与智能体等前沿领域，在相关方向累计开源模型与数据集下载量超百万次，研究成果发表于Nature Machine Intelligence、Nature Communications、ICLR、NeurIPS、ACL、KDD等国际会议期刊，长期担任会议AC，以及并持续参与国际开源社区建设。团队注重“科研 + 工程”双能力培养，鼓励学生参与高水平论文发表、开源项目与产业合作。
电子邮箱：wulijun@pjlab.org.cn
个人主页： https://apeterswu.github.io/', email = 'wulijun@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wulijun';
UPDATE dtlms_users SET email = 'wulijun@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wulijun' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '周伯文教授具备丰富的国际化科学研究与管理经验，研究方向为语音和自然语言处理、多模态与知识表征、理解、生成、推理、人机对话、可信赖AI等，他长期开展人工智能国际前沿基础理论研究、技术创新、人才培养及大规模产业化应用，形成了国际视野下从学术、教育到产业全链路的产学研用融合特色范式，入选国家千人计划，荣获我国智能科学最高奖“吴文俊人工智能杰出贡献奖”等。
在国际一流期刊及顶级学术会议上已发表上百篇论文，引用数万次包括多篇开拓性论文单篇他引数千次，在人工智能技术和产业界大规模应用核心领域取得杰出成就，有较高的国际影响力。2016年，周伯文教授带领团队在国际上首次提出与下游任务无关的自注意力与多头机制等表征新机理与新方法，奠定了Transformer架构的理论基础之一，推动通用人工智能、语言大模型表征新进展，是实现生成式AI的重要里程碑。周博士其他两篇生成式AI代表性论文总计被引超5000余次。产业落地上，曾先后领导了IBM Watson平台及京东NeuHub平台的技术路线，推动了人工智能技术在产业界的大规模商业化。2003年，牵头研制出了世界第一个完全嵌入式的大词汇量的语音到语音双向实时翻译系统，支持几十种语言，被IBM客户和外界开发者广泛用于实体经济垂直行业。
电子邮箱：admissions@pjlab.org.cn （请明确说明意向选择周伯文教授作为导师）', email = 'zhoubowen@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhoubowen';
UPDATE dtlms_users SET email = 'zhoubowen@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhoubowen' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '宋纯锋，上海人工智能实验室青年科学家，负责AGI4S科学数据智能体与AI4Neuroscience研究。博士毕业于中国科学院自动化所，后留所工作历任助研、副研，2023年加入上海人工智能实验室。现已发表高水平学术论文50余篇（其中第一作者单篇引用过百论文5篇，谷歌学术引用4700余次，连续4年入选斯坦福大学发布的全球前2%顶尖科学家榜单，入选上海市东方英才拔尖项目、中科院特别研究助理资助等人才项目，担任IEEE高级会员、中国计算机学会计算机视觉专委会（CCF-CV）委员等学术工作。（个人主页：https://cf-song.github.io/）欢迎邮件联系：songchunfeng@pjlab.org.cn', email = 'songchunfeng@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'songchunfeng';
UPDATE dtlms_users SET email = 'songchunfeng@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'songchunfeng' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '张伟楠
zhangweinan@pjlab.org.cn
https://scholar.google.com/citations?hl=en&user=Qzss0GEAAAAJ
张伟楠博士现任上海人工智能实验室物理智能中心负责人，上海交通大学计算机学院教授、博士生导师，国家自然科学基金青B项目获得者，科研领域包括强化学习、具身智能、智能体，当前主要研究大模型多智能体基础共性技术和一脑多形机器人泛化控制技术，相关研究成果在CCF-A类国际会议和期刊上发表100余篇学术论文，谷歌学术引用3万余次，H指数87，爱思唯尔中国高被引学者，出版教材《动手学强化学习》和《动手学机器学习》等销量超6万册。张伟楠长期担任NeurIPS、ICML、ICLR、KDD等会议的领域主席和TPAMI等期刊的编委，主持重大项目课题，获得吴文俊人工智能优秀青年奖和达摩院青橙奖。', email = 'zhangweinan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangweinan';
UPDATE dtlms_users SET email = 'zhangweinan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangweinan' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '张奇，复旦大学计算与智能创新学院教授、国家级领军人才。兼任上海市智能信息处理实验室副主任，中国中文信息学会理事、CCF 大模型论坛常务委员、CIPS 大模型专家委员会委员、CIPS 信息检索专委会常务委员。主要研究方向是自然语言处理和信息检索，聚焦大语言模型、自然语言表示、信息抽取、鲁棒性和解释性分析等。在ACL、EMNLP、COLING、全国信息检索大会等重要国际国内会议多次担任程序委员会主席、领域主席、讲习班主席等。近年来承担了国家重点研发计划课题、国家自然科学基金、上海市科委等多个项目，在国际重要学术刊物和会议发表论文200余篇，获得美国授权专利4项，著有《自然语言处理导论》和《大规模语言模型：理论与实践》，作为第二译者翻译专著《现代信息检索》。获得WSDM 2014最佳论文提名奖、COLING 2018 领域主席推荐奖、NLPCC 2019杰出论文奖、COLING 2022杰出论文奖，ACL 2025杰出论文奖。获得上海市“晨光计划”人才计划、复旦大学“卓越2025”人才培育计划等支持，获得钱伟长中文信息处理科学技术一等奖、汉王青年创新一等奖、上海市科技进步二等奖、教育部科技进步二等奖、ACM 上海新星提名奖、IBM Faculty Award等奖项。   https://scholar.google.com/citations?user=XfqR3yYAAAAJ&hl=en
邮箱：qz@fudan.edu.cn', email = 'zhangqi@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangqi';
UPDATE dtlms_users SET email = 'zhangqi@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangqi' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET email = 'zhangwenwei@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangwenwei';
UPDATE dtlms_users SET email = 'zhangwenwei@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangwenwei' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '张超，清华大学电子工程系副教授、博士生导师，上海人工智能实验室双聘青年科学家，伦敦大学学院（UCL）脑科学部荣誉副教授。主要研究方向包括多模态大语言模型、脑信号解码与通用时间序列智能等。毕业于清华大学计算机系，并获英国剑桥大学工程系博士学位，曾任京东语音组负责人、Google 研究科学家等职务，相关技术已广泛应用于语音交互、音视频理解、推荐系统及金融预测等领域。团队近年来研发了 SALMONN 系列音视频大语言模型、BrainOmni 脑信号基础模型等代表性成果。在NeurIPS、ACL、ICASSP等语音语言和人工智能领域顶级会议及 Nature、Cell 子刊发表论文百余篇，6 次获最佳学生论文奖，并担任多项国内外重要学术兼职。

邮箱：zhangchao@pjlab.org.cn
个人主页：http://mi.eng.cam.ac.uk/~cz277', email = 'zhangchao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangchao';
UPDATE dtlms_users SET email = 'zhangchao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangchao' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '张铂，目前任上海人工智能实验室-青年科学家，科学智能体团队负责人，入选上海市高层次人才计划拔尖项目。专注于通用智能体、多模态推理科学模型及其在AI自主科学发现等领域的研究，已在CVPR /ICLR/T-PAMI等国际顶级会议和期刊发表学术论文50余篇，谷歌学术4900余次引用。他在曾获北美Waymo挑战赛冠军、OpenAI MLE冠军；研发了通用智能体自主科学发现系统框架InternAgent、科学发现平台书生Intern-Discovery（获实验室奥斯卡奖），并在WAIC-2025成功发布，相关成果被新华网、人民网、新民晚报、麻省理工科技评论等多家权威媒体报道，浏览量超过百万；基于Intern-Discovery平台，与临港实验室合作研发元生OriGene，成功发现GPR160和ARG2两个原创靶点并进入临床应用。此外，研发了通用科学文献解析工具MinerU/MinerU-2.5，通用多模态推理模型InternVL等知名开源项目，累计获得Github开源社区星标数量超60K。主页：https://bobrown.github.io/boZhang.github.io/
电子邮箱:zhangbo@pjlab.org.cn', email = 'zhangbo@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangbo';
UPDATE dtlms_users SET email = 'zhangbo@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangbo' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '成宇博士目前负责新一代大语言模型/多模态大模型的研发。从2021年开始到2023年，任微软雷德蒙德研究院首席研究员，带领团队和OpenAI团队紧密合作，对GPT系列模型进行了效率、鲁棒性和扩展性优化，推动相关服务和应用的产品化，包括以GPT-4作为主要模型的New Bing、由GPT-3.5提供后台服务的Github Copilot以及由DALL-E-2提供支持的Image Creator。入选国家、上海市海外人才引进计划。担任人工智能顶会如ICML和NeurIPS的高级领域主席，顶级期刊TMLR责任编辑，以及CVPR,ICLR, ACL, ACMMM和NAACL的领域主席。论文曾获得NeurIPS 2023 杰出论文奖、IEEE SPS 年度最佳论文奖、WACV 2021 最佳学生论文荣誉奖和SDM 2015 最佳论文入围奖。谷歌学术总引用30348，h-index：81', email = 'chengyu@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'chengyu';
UPDATE dtlms_users SET email = 'chengyu@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'chengyu' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '个人主页：https://liyn.site/
google scholar：https://scholar.google.com/citations?user=y_cp1sUAAAAJ
个人介绍：
上海人工智能实验室大模型中心青年科学家，上海交通大学兼职导师，入选上海市东方英才拔尖人才项目。分别在香港中文大学和清华大学获得博士、学士学位。目前研究主要关注 LLM post-training、agentic system、data efficiency 等方向。', email = 'liyining@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'liyining';
UPDATE dtlms_users SET email = 'liyining@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'liyining' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '李恒杰，浦江国家实验室高级工程师，上海交通大学电院兼职博导，上海创智学院全时导师。研究方向包括并行计算、先进编译技术、软硬件协同优化。所带领团队在AI软件栈国产适配、AIGC模型算法加速系统构建方面有深厚积累，如国产AI System（DeepLink:  https://github.com/DeepLink-org）、三维实景重建系统（LandMark: https://github.com/InternLandMark/LandMark）、机器人训练数据自动生成系统（Nimbus: https://github.com/DeepLink-org/Nimbus）、视频生成的训推系统（训练加速LiteGen: https://github.com/Vchitect/LiteGen 推理加速Jano: https://github.com/chen-yy20/Jano），相关成果发表在NeurIPS, CVPR, SIGGRAPH Asia, HPDC, TACO等重要会议及期刊。目前主要感兴趣方向在超智融合计算体系建设方面。
电子邮箱：lihengjie@pjlab.org.cn', email = 'lihengjie@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'lihengjie';
UPDATE dtlms_users SET email = 'lihengjie@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'lihengjie' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '上海人工智能实验室Al for Science中心联合负责人&物质科学团队负责人、青年科学家、上海创智学院全时导师、复旦大学计算与智能创新学院兼职博士生导师，担任科学通报、Sci.Bull.、Chin.Chem.Lett.等期刊青年编委。主要从事AI for 化学、材料学、谱学研究，在上海AI实验室领导开发了ChemLLM化学大语言模型系列及CrystalX晶体结构解析模型。以通讯作者在Nat.Catal.、JACS、Angew、ICLR、CVPR、ACL、AAAI、KDD等化学类顶级期刊和人工智能会议发表论文20余篇。获得上海市东方英才计划资助。
https://scholar.google.com/citations?user=RQqws5gAAAAJ&hl=zh-CN
邮箱:liyuqiang@pjlab.org.cn', email = 'liyuqiang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'liyuqiang';
UPDATE dtlms_users SET email = 'liyuqiang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'liyuqiang' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '2025年度吴文俊人工智能科学技术奖（自然科学奖）获得者，曾获得上海市超级博士后、东方英才等项目资助。杨超博士目前主要从事AI安全可信、智能体系统、机器人交互与智能决策方面的研究工作，目前发表人工智能相关学术论文60余篇，研究成果主要收录于NeurIPS，CVPR，ICLR等一系列人工智能顶级会议，在谷歌学术上总引用量超过7000余次，其安全对齐领域工作曾荣获ACL 2024 Outstanding Paper Award，曾在清华大学带队于2016、2019年机器人顶级会议IROS国际机器人抓取与操作比赛中荣获机器人分拣、机器人服务、机器人桌面整理等多项国际冠军，力压MIT等其他参赛队伍；其提出的模仿学习理论荣获NeurIPS Spotlight并一直延续至后来的AI大模型RLHF、RLVR等，成为大模型后训练的重要推手。
个人邮箱：yangchao@pjlab.org.cn
个人网站：https://emigmo.github.io/', email = 'yangchao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'yangchao';
UPDATE dtlms_users SET email = 'yangchao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'yangchao' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '林达华于2012年在美国麻省理工学院获得计算机科学博士学位，研究领域涵盖计算机视觉、深度学习、大模型和生成式AI等。在人工智能相关顶级学术会议与期刊发表逾300篇论文，在2010年获得NeurIPS的最佳学生论文奖。曾多次担任CVPR、ECCV、ICCV、ACM Multimedia与AAAI等主要国际会议的领域主席及计算机视觉主要国际期刊IJCV编委。近年来主要专注于人工智能基础设施和大模型技术研发等工作，带领团队发展出SenseParrots深度学习框架、OpenMMLab计算机视觉算法开源体系、DeepLink人工智能开放计算体系、InternLM书生浦语等一系列在业界有重要影响的项目。在生成式AI领域，指导学生和团队发展出CityNeRF、AnimateDiff、PointLLM等具有广泛影响力的开创式算法体系。', email = 'lindahua@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'lindahua';
UPDATE dtlms_users SET email = 'lindahua@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'lindahua' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '2022年GJ级海外高层次人才引进计划，2021年SH海外高层次人才引进计划，2021年获得澳大利亚未来学者杰出青年人才计划和悉尼大学杰出科研校长奖。据2021年国际权威机构爱斯维尔对计算机视觉与模式识别领域2016-2021发表论文的统计，其平均每篇文章引用次数（Citations per paper）和领域加权影响力（field-weighted citation impact，FWCI）皆为澳大利亚第1、世界前10（其中FWCI第10为牛津大学英国皇家协会院士A. Zisserman）。
在TPAMI、IJCV、CVPR、NeurIPS等CCF A类期刊和会议论文发表200余篇，据谷歌学术统计，截止到2023年11月，论文总引用超57,000次（近五年为46,143），H-Index为106（近五年为100），其中86篇文章引用次数超过100，授权专利65项。
他带领团队联合中国科学技术大学、上海交通大学等科研机构研发了全球中期天气预报大模型“风乌”，首次实现全球气象有效中期预报时间突破10天，超过欧洲气象局、美国气象局及其他AI气象大模型；升级版“风乌GhR”在此基础上，实现首个人工智能驱动的9千米分辨率预测，达到世界领先水平。发布了国际首个化学领域的开源大语言模型“浦科化学（ChemLLM）”，九项化学核心能力全面超过GPT-3.5，与GPT-4相当。发布了首个种业大语言模型“丰登（SeedLLM）”，填补我国在AI育种领域的技术空白。开发了首个大规模势函数预训练方法，使得分子动力学模拟仅需过去百分之一的计算资源就可达到相同精度。完成了国际性能最优的量子算法模拟，打破谷歌最初提出的“量子霸权”主张。设计了射电星系发现模型，基于此我国天文学家提出了新的星系宇宙学理论。
邮箱：admissions@pjlab.org.cn （请明确说明意向选择欧阳万里教授作为导师）', email = 'ouyangwanli@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'ouyangwanli';
UPDATE dtlms_users SET email = 'ouyangwanli@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'ouyangwanli' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '沈春华聚焦多模态模型、生成模型、具身智能、空间感知等方向研究。入选教育部长江讲席教授计划。所指导学生中有数十名毕业生顺利进入知名高校（新加坡NTU、悉尼大学、阿德莱德大学）和头部科技企业深耕技术研发，成长为领域骨干人才。他的谷歌学术引用超过 10 万，H index 150. 主页：https://cshen.github.io/', phone_number = '18899997777', email = 'shenchunhua@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'shenchunhua';
UPDATE dtlms_users SET phone_number = '18899997777', email = 'shenchunhua@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'shenchunhua' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET email = 'shenyuan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'shenyuan';
UPDATE dtlms_users SET email = 'shenyuan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'shenyuan' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '滕妍，上海人工智能实验室安全可信AI中心青年科学家，目前主要从事大模型和智能体的安全攻防与评测方向，重点关注大模型在复杂应用场景落地的实际安全问题与解决方案。关注交叉学科AI安全探索，涵盖认知心理、伦理治理等。近2年发表大模型安全相关论文30余篇，多篇收录于ICML、ICLR、NeurIPS、ACL、AAAI、EMNLP、ICCV等（主页链接：https://tengyan666.github.io/）
邮箱:tengyan@pjlab.org.cn', email = 'tengyan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'tengyan';
UPDATE dtlms_users SET email = 'tengyan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'tengyan' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '王利民，上海人工智能实验室／南京大学计算机学院双聘教授，博士生导师，国家级青年人才计划入选者。研究领域为计算机视觉和多模态大模型，在IJCV、T-PAMI、CVPR、ICCV、NeurIPS等期刊和会议发表论文100余篇，谷歌学术引用4.8万余次，两篇一作论文引用超过4000次。主持江苏省自然科学基金攀登项目等。带领团队研发了首个通用视频理解大模型体系InternVideo，全球用户下载量超过600万，被Google、Meta、NVIDIA等知名企业使用，产生了重要国际影响力。曾获得广东省技术发明一等奖，蚂蚁InTech科技奖，ACM MM 2023唯一最佳论文提名奖、首届世界人工智能大会青年优秀论文奖。担任CVPR/ICCV/NeurIPS等会议的领域主席和TPAMI/IJCV等期刊的编委。
电子邮箱:lmwang@nju.edu.cn', phone_number = '13600000000', email = 'wanglimin@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wanglimin';
UPDATE dtlms_users SET phone_number = '13600000000', email = 'wanglimin@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wanglimin' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '王斌，上海人工智能实验室青年科学家、上交AI学院兼职博导、东方英才拔尖人才。专注多模态大模型、智能文档理解与 Data-Centric AI，带队打造文档解析领域 Top1 开源项目 MinerU，模型下载近千万次；构建OmniDocBench，被 Gemini、OpenAI、DeepSeek、Qwen 等作为基础评测榜单。顶会论文 50 余篇，引用 5000+。欢迎自驱力强、渴望做出影响力研究的同学加入！
 
联系方式：
邮箱：wangbin@pjlab.org.cn
GitHub：wangbinDL - Overview
Google Scholar：https://scholar.google.com/citations?user=WljXYoYAAAAJ', email = 'wangbin@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangbin';
UPDATE dtlms_users SET email = 'wangbin@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangbin' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '王毅，上海人工智能实验室青年科学家，长期专注多模态大模型与视频前沿研究，致力于打造真正看懂世界的智能系统。主导或参与开源InternVideo、VideoChat、InternVL、Intern-S等模型或系统，相关成果发表于ICLR、NeurIPS、CVPR等顶会。欢迎对多模态大模型、智能体和世界模型充满热情的同学加入，一起探索前沿、做出有国际影响力的工作。
邮箱：wangyi@pjlab.org.cn
Google Scholar：https://scholar.google.com/citations?user=Xm2M8UwAAAAJ', email = 'wangyi@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangyi';
UPDATE dtlms_users SET email = 'wangyi@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangyi' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '王潚崧，AI4S中心青年科学家，长期从事生物医药相关科研工作（~20年），曾就职NIH和Nvidia。共发表论文60余篇，专著1本，专利20余项，谷歌学术引用14000+。具备比较丰富的学生指导经验，想做有用、有趣工作的同学看过来！
wangxiaosong@pjlab.org.cn
https://scholar.google.com/citations?user=c66GnOEAAAAJ&hl=en', email = 'wangsusong@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangsusong';
UPDATE dtlms_users SET email = 'wangsusong@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangsusong' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET email = 'wangyingchun@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangyingchun';
UPDATE dtlms_users SET email = 'wangyingchun@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangyingchun' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '白磊现任上海人工智能实验室青年科学家、科学智能中心负责人，主要研究科学多模态模型、科研智能体及其在跨学科领域的应用。入选国家高层次人才引进计划，获DAI最佳论文奖、IEEE-TCSVT最佳论文奖、云帆奖、Google 博士奖等。主导或参与研发Intern-S系列科学基础模型、InternAgents科学智能体系统、InternDiscovery科学发现平台等实验室代表成果。邮箱：bailei@pjlab.org.cn', email = 'bailei@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'bailei';
UPDATE dtlms_users SET email = 'bailei@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'bailei' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '瞿晶晶博士现任上海人工智能实验室青年科学家、东方英才人才入选者，Epitome 人工智能社会实验平台创始人。长期深耕通用人工智能、多智能体系统、AI 治理与社会实验交叉前沿领域，主持负责新一代多智能体操作系统整体研发工作。牵头承担重大项目及省部级科研课题共计二十余项，深耕行业前沿技术攻关，全力推进多智能体底层基座架构迭代优化、异构智能体互联互通、大规模智能体集群高效调度等核心技术突破。在多智能体交互推理、分布式协同架构、可信智能体安全管控等领域形成深厚学术积累，发表多篇高水平学术论文，科研成果扎实丰硕。其研究成果深度赋能科学智能、产业数字化转型、云端协同部署等多元应用场景，持续打通理论研究、技术研发与场景落地全链条，有力推动新一代多智能体操作系统实现工程化落地与规模化产业应用，为通用人工智能产业高质量发展筑牢技术根基。
邮箱地址：qujingjing@pjlab.org.cn', email = 'qujingjing@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'qujingjing';
UPDATE dtlms_users SET email = 'qujingjing@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'qujingjing' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '石博天，上海人工智能实验室青年科学家，前沿探索中心管理委员会成员，知识前沿团队负责人；上海创智学院全时双聘副研究员；上海交通大学兼职博导。入选上海市启明星、东方英才等人才项目，在NeurIPS、ICLR、ACL、ICCV、ECCV、CVPR等学术会议期刊发表学术论文50余篇。研究方向包括多模态大模型、智能体系统与自动驾驶等。作为最早提出将LLM/VLM与智能体（记忆与自主反思等机制）应用于自动驾驶与道路场景理解的团队之一，提出的一系列工作背OpenAI等机构关注，部分技术路线（如基于场景重建与交通流模拟的闭环仿真引擎等）正在逐渐被工业界采纳，为落地量产提供技术方向。目前的重点研究方向为自主终身学习智能体系统，早于Anthropic推出的Skills，发表了基于自主反思与经验学习的自主进化智能体系统MUSE，成为与Google、Meta、DeepMind、OpenAI等同期（2025年9-10月）发布的系列工作之一。
邮箱：shibotian@pjlab.org.cn
Google Scholar：https://scholar.google.com/citations?user=K0PpvLkAAAAJ&hl=en', email = 'shibotian@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'shibotian';
UPDATE dtlms_users SET email = 'shibotian@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'shibotian' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '穆尧，上海交通大学长聘教轨助理教授，入选国家级青年人才计划，上海市海外高层次青年人才，上海人工智能实验室双聘研究员，智源青年学者， EAI-100 2025学术新锐。博士毕业于香港大学计算机系，访学于苏黎世联邦理工学院、新加坡国立大学等。穆尧博士长期从事具身智能的基础研究，深耕多模态具身认知、具身世界模型和具身自主进化系统等方向，担任了NeurIPS、ICLR等国际机器学习顶级会议的领域主席，中国计算机学会智能机器人专委会执委，中国图形图像学会三维视觉专委会专委，Valse执行领域主席，在IJRR、RSS、NeurIPS、ICML、CVPR等计算机领域国际顶级期刊和会议发表论文50余篇，谷歌学术引用超3800余次。曾荣获2026年ICRA最优论文奖提名、2025年IROS最优论文奖提名、2024年ECCV协同具身智能研讨会最优论文奖、2024年中国自动化学会自主机器人研讨会奖学金（全国5人）、2021年IEEE ICCAS2020大会最优学生论文奖、IEEE IV2021最优学生论文提名奖等多项奖励。个人主页：https://www.cs.sjtu.edu.cn/jiaoshiml/muyao.html Google Scholar：https://scholar.google.com/citations?user=HK4x3fkAAAAJ&hl=en 邮箱：muyao@sjtu.edu.cn', email = 'muyao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'muyao';
UPDATE dtlms_users SET email = 'muyao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'muyao' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '翟少鹏博士目前关注具身大模型后训练，在真实世界交互中强化学习。博士期间开发的研发的多目标混合整数优化算法在国家电网（西南分部）试运行，实际服务四川、重庆、西藏三省的电力系统调度。从2020年开始到2022年，任网易人工智能实验室强化研究员，研发的智能体累计服务百万人次。2022年至今在浦江实验室负责具身大模型和决策模型的研究，研发的openPaL开放任务智能体，首次在不依赖人类数据情况下，在多智能体实时任务场景下达到顶尖人类水平。服务于世界最大的自动化码头（洋山港四期）智能化调度，支撑该港口达成700万集装箱年吞吐量。累计发表论文20篇，其中SCI、顶会共12篇。
zhaishaopeng@pjlab.org.cn', email = 'dishaopeng@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'dishaopeng';
UPDATE dtlms_users SET email = 'dishaopeng@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'dishaopeng' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '翟广涛，上海交通大学特聘教授，上海人工智能实验室双聘研究员，IEEE Fellow，国家杰青，Clarivate高被引学者，多年从事多媒体智能相关研究，获IEEE TMM和TBC期刊最佳论文奖等国际奖励30余项。以第一完成人获得中国电子学会自然科学一等奖、技术发明一等奖及中国图象图形学学会技术发明一等奖等，主持国家自然科学基金重点、国家重点研发计划、国家科技重大专项等项目。任Elsevier Displays和IEEE OJID期刊主编、上海市图像图形学学会理事长。https://scholar.google.com/citations?hl=en&user=E6zbSYgAAAAJ&view_op=list_works&sortby=pubdate
电子邮箱:zhaiguangtao@sjtu.edu.cn', email = 'diguangtao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'diguangtao';
UPDATE dtlms_users SET email = 'diguangtao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'diguangtao' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '胡侠老师现任上海 AI Lab 领军科学家、主任助理，曾任美国莱斯大学正教授。他现在的研究关注于基座大模型、智能体、及AI系统方向。他曾获 SIGKDD 2021 Raising Star 称号，带领团队在SysML、 ICML、WWW 等顶会多次获得或提名最佳论文，谷歌学术引用 4 万余次，Github开源项目stars 2万余次。胡老师课题组开发了多个著名开源项目及奠基工作，如 AutoKeras、DouZero、NCF 等，毕业的博士现于 OpenAI，XAI 等顶尖AI企业或罗格斯大学等知名高校工作。感兴趣的同学欢迎发送简历到wuxuansheng@pjlab.org.cn，在邮件正文可以写一句话的亮点！', email = 'huxia@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'huxia';
UPDATE dtlms_users SET email = 'huxia@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'huxia' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET email = 'huyang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'huyang';
UPDATE dtlms_users SET email = 'huyang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'huyang' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '胡舒悦博士毕业于香港中文大学，长期从事智能体、多智能体系统及大模型方向的研究。在 PNAS、National Science Review、AAAI、IJCAI、NeurIPS、ICML、AAMAS 国际知名期刊会议上发表论文 60 余篇。成果获中国电子学会自然科学奖一等奖、国际分布式人工智能会议DAI 2025唯一最佳论文、多智能体系统顶会AAMAS 2026最佳学生论文奖提名。担任多智能体系统顶会 AAMAS 2024组委会成员（大陆第四位）与领域主席，国际知名期刊 JAAMAS、Neurocomputing 客座编辑，长期担任多个人工智能国际知名会议程序委员会（高级）委员。入选 2023 年度上海市海外高层次人才计划。联系邮箱：shuyuehu217@gmail.com。', email = 'hushuyue@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'hushuyue';
UPDATE dtlms_users SET email = 'hushuyue@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'hushuyue' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '博士毕业于英国牛津大学计算机科学系，入选国家级、上海市高层次人才计划,获第十七届浦江创新论坛“青年先锋”称号。主要研究方向是科学智能（AI for Science)，包括科学多模态大模型、科研智能体系统、大模型技术的科学应用（如基因语言模型、蛋白质语言模型等)。在ACL、ICML, NeuIPS、ICLR等国际期刊和会议发表文章40余篇，相关成果入选科技日报“十四五硬核成果"、新华社“2025上海科技十大瞬间”、被人民日报、新华社、央视新闻等主流媒体多次报道。
dongnanqing@pjlab.org.cn', email = 'dongnanqing@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'dongnanqing';
UPDATE dtlms_users SET email = 'dongnanqing@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'dongnanqing' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '蔡品隆，前沿探索中心青年科学家，研究聚焦知识结构化表征、知识驱动推理与智能体系统。热忱欢迎怀揣 AGI 愿景、勤于钻研、勇于实践，致力 AI 技术落地应用的学子加入，并肩开拓科研新高度。
邮箱：caipinlong@pjlab.org.cn
个人主页：https://caipinlong.top/
谷歌学术主页：https://scholar.google.com.hk/citations?user=H6mQGfAAAAAJ&hl=zh-CN', email = 'caipinlong@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'caipinlong';
UPDATE dtlms_users SET email = 'caipinlong@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'caipinlong' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '薛天帆教授是实验室前沿中心视觉生成处理团队负责人、和香港中文大学讯息工程系MMLab的校长助理教授。在此之前，他在谷歌研究院的计算摄影团队担任主任工程师，工作了五年以上，有着丰富的产学结合经验。他毕业于麻省理工学院计算机科学与人工智能实验室。他的研究重点是计算摄影和生成式AI，研究的反射光技术被谷歌Photoscan应用，拥有超过1000万用户，研究的快速双边学习已被集成到谷歌Tensor芯片中。这是他的主页
https://tianfan.info/
项目github: https://github.com/OpenImagingLab
邮箱: tianfan.xue@gmail.com', email = 'xuetianfan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'xuetianfan';
UPDATE dtlms_users SET email = 'xuetianfan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'xuetianfan' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '赵斌，zhaobin@pjlab.org.cn，上海人工智能实验室物理智能中心AC，青年科学家。从事具身智能研究，致力于构建人形、轮式、旋翼等异构智能体协同系统。在国际期刊和会议发表学术论文 80 余篇，谷歌引用6200余次。获中国科协青年托举人才工程，国家一级学会科技奖。相关成果应用于航空航天、应急救援、城市反恐等任务中，公开技术被 Asia Times、The SUN、人民日报、新华网等国内外媒体报道。https://scholar.google.com.hk/citations?user=DQB0hqwAAAAJ&hl=zh-CN', email = 'zhaobin@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhaobin';
UPDATE dtlms_users SET email = 'zhaobin@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhaobin' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '邱剑涛，清华大学电子工程博士，现任上海人工智能实验室青年科学家，长期从事大模型数据与后训练、多模态文档理解和文档解析研究，在真实场景中推进数据、模型与系统闭环。欢迎有研究热情和工程能力的同学联系。
Email qiujiantao@pjlab.org.cn
Github darkrush - Overview
Google Scholar https://scholar.google.com/citations?hl=zh-CN&user=Vm8bStkAAAAJ', email = 'qiujiantao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'qiujiantao';
UPDATE dtlms_users SET email = 'qiujiantao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'qiujiantao' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '邵婧，现任上海人工智能实验室安全可信AI中心联合负责人，青年科学家，兼上海交通大学、复旦大学博士导师。博士毕业于香港中文大学MMLab，曾任商汤科技研究总监。研究自主、可控、可信AI，聚焦多种模态大模型及智能体安全评估与价值对齐相关研究工作。累计发表论文近100篇，引用14000余次，连续两年指导学生于ACL2024、2025获得Outstanding Paper Award，2023~2025连续三年入选斯坦福前2%科学家榜单。培养理念：我带你看科研的门道，你带我看世界的年轻——亦师亦友，一起成长。
主页：https://amandajshao.github.io/
邮箱：shaojing@pjlab.org.cn', email = 'shaojing@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'shaojing';
UPDATE dtlms_users SET email = 'shaojing@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'shaojing' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '邹娜博士现任上海AI Lab青年领军科学家，前美国教授+AI公司联合创始人，手握650万美元经费，专攻可解释、可信赖和可验证的AI安全系统及医疗场景验证，成果发表在ICLR/NeurIPS/ICML，且拿过NSF CAREER、IEEE Kaufman等大奖。真实难题+成长型导师+顶级平台，博士们，等你来加入！
电子邮箱：zouna@pjlab.org.cn', email = 'zouna@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zouna';
UPDATE dtlms_users SET email = 'zouna@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zouna' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '郝红霞博士现任上海人工智能实验室青年科学家，负责了实验室AI+材料方向的高峰项目。2022-2025年在微软研究院资深研究员期间，参与微软内部AI for Materials重点项目研发，领导冲刺125个科学问题; 团队开发的通用原子级科学基础模型 MatterSim取得国际上材料基础大模型综合效果最佳的突破; 生成式材料设计 MatterGen被Nature接收，1年多引用超800，已成为领域内标志性成果; 微软内部hackathon比赛团队获得第一名，得到了向微软CEO，CTO汇报工作的机会。博士/博士后期间，针对复杂界面与限域体系机理和材料高精度模拟中的关键问题，取得了一系列开创性和奠基石的成果。如所承担的微液滴化学机理研究，获得美国MURI支持，是2021年度化学领域唯一一个获支持项目，理论上首次定量证实气-水微界面存在高达约16 MV/cm 的强内建电场，揭示了界面电场及其波动对微液滴化学反应加速的重要作用，为相关机理争议提供了定量解释。相关成果发表于 【第一作者，Nature Communications（2022）】，入选“编辑亮点”，并被 Science、J. Am. Chem. Soc.、PNAS 等持续引用（近300次），如液滴化学奠基人Richard Zare院士和 R. Graham Cooks 教授多次正面引用。近5年，申请人人在 Nature Communications、J. Am. Chem. Soc.、Angew. Chem. Int. Ed.等发表第一/通讯作者论文4篇，另外作为微软AI for Science团队的核心骨干，参与开发的工业成果联合发表在Nature、Nature Machine Intelligence及公开于arXiv等8篇（含通讯作者2篇）；申请发明专利2项，实验验证新材料2种。相关研究涵盖基础机理、模型方法、材料发现和应用验证等环节。在顶级期刊上共发表 30 余篇论文，谷歌学术引用超过 3400，h-index 为21。Google Scholar link: https://scholar.google.com/citations?user=9Mugj9oAAAAJ&hl=zh-CN
电子邮箱:haohongxia@pjlab.org.cn', email = 'haohongxia@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'haohongxia';
UPDATE dtlms_users SET email = 'haohongxia@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'haohongxia' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET email = 'guoqipeng@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'guoqipeng';
UPDATE dtlms_users SET email = 'guoqipeng@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'guoqipeng' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '陆超超，安全可信AI中心联合负责人，上海交通大学和复旦大学兼职博导，先后获南京大学学士、香港中文大学硕士、剑桥大学博士学位。分别入选国家级及上海市海外高层次人才引进计划（青年）。曾获AAAI首届唯一最佳学生论文奖、香港中文大学工程学院唯一最佳毕业论文奖，早期研发的人脸识别算法准确率首次超越人类并获《自然》《科学》等报道。其在大模型因果推理、因果可解释性、视觉因果理论和高阶认知安全等方向取得系列原创成果，也构建了全球首个大模型因果能力评测体系。面向大模型安全，牵头构建内生安全体系SafeWork，在金融、核安全、医疗、能源等高风险行业落地应用，并获国内外机构与专家高度评价。积极参与IDAIS、SCAI等国际AI安全对话，与诺贝尔奖得主Geoffrey Hinton、图灵奖得主Yoshua Bengio、图灵奖得主姚期智等国内外专家共同讨论形成并签署“威尼斯共识”“新加坡共识”“上海共识”“伦敦共识”，为安全可信AI贡献中国方案。现阶段主要从事大模型和智能体因果推理与安全可信研究，目标是赋予大模型和智能体因果推理能力，构建因果世界模型、打造自动化的智能科学家、创造具有自我意识的智能体，为实现自主、安全、可信的通用人工智能探索一条新的路径。邮箱地址：luchaochao@pjlab.org.cn', email = 'luchaochao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'luchaochao';
UPDATE dtlms_users SET email = 'luchaochao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'luchaochao' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '陈恺现任上海人工智能实验室大模型中心负责人，青年领军科学家，在语言和多模态大模型等方向有丰富研究经验，在人工智能方向顶级会议和期刊上发表论文100多篇，谷歌学术引用超过3.6万次。带领团队负责书生（Intern）系列大模型的研发工作，并从零建立了早期OpenCompass司南评测体系，以及OpenMMLab计算机视觉开源算法体系，累计获得超过14万GitHub star，形成了广泛的国际影响力。
邮箱：chenkai@pjlab.org.cn
Google Scholar：https://scholar.google.com/citations?user=eGD0b7IAAAAJ', phone_number = '13900000000', email = 'chenkai@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'chenkai';
UPDATE dtlms_users SET phone_number = '13900000000', email = 'chenkai@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'chenkai' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '陈昕苑博士是上海人工智能实验室担任青年科学家，上海交通大学、复旦大学兼职博士导师。从事生成模型，图像视频生成，世界模型，计算机视觉方向研究，特别是交互式视频生成、长视频生成、物理世界模拟器等领域。2020年6月获上海交通大学和悉尼科技大学双学位博士。在CVPR、ICCV、Nuerips、ICML、ICLR等计算机视觉和机器学习相关领域顶会发表论文数十篇。主持多项国家自然科学基金、省部级科研项目，入选上海市启明星人才计划。欢迎有自我驱动并对生成模型和世界模型感兴趣的同学加入。
谷歌学术：https://scholar.google.com/citations?user=3fWSC8YAAAAJ&hl=en
邮箱:chenxinyuan@pjlab.org.cn', email = 'chenxinyuan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'chenxinyuan';
UPDATE dtlms_users SET email = 'chenxinyuan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'chenxinyuan' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '面向下一代可信智能系统，课题组聚焦大模型与智能体的可解释性、可控生成与安全对齐，致力于推动模型从“会生成”迈向“可理解、可干预、可治理”，探索智能系统在真实复杂场景中安全、可靠、可持续发展的关键问题。
本人现任西安交通大学助理教授、AI Lab 双聘教师，入选陕西省人才引进计划。相关研究成果发表于 TPAMI、ICML、NeurIPS、ICLR等国际顶级会议与期刊，Google Scholar 引用 2000+。
课题组重视深度指导与长期成长，定期开展高质量一对一研究讨论，围绕研究方向凝练、技术路线设计、实验结果复盘与论文写作进行系统训练。如果你希望在大模型时代研究真正关键、长期且富有挑战的问题，欢迎加入我们，共同探索可信智能的科学基础与未来边界。
邮箱：denghq7@xjtu.edu.cn
Google Scholar: https://scholar.google.com/citations?user=QEjqzXgAAAAJ&hl=en', updated_at = CURRENT_TIMESTAMP WHERE username = 'denghuiqi';
UPDATE dtlms_user_profiles SET introduction = '研究通用人工智能的理论、方法、模型和系统，致力于开发连接计算空间和物理世界的通用智能基础方法。
- 邮箱：dingning@mail.tsinghua.edu.cn；
- 谷歌学术主页：https://scholar.google.com/citations?user=uZXQuYAAAAAJ&hl=zh-CN。', updated_at = CURRENT_TIMESTAMP WHERE username = 'dingning';
UPDATE dtlms_user_profiles SET introduction = '董峻廷，浙江大学博士，现任上海人工智能实验室研究员。主要研究方向包括世界模型、具身智能与空间智能，致力于构建具备三维空间理解、动态场景建模与动作推理能力的智能系统。近年来在 CVPR、ICCV、ECCV、NeurIPS、SIGGRAPH Asia、RSS、TPAMI、IJCV 等人工智能与计算机视觉顶级会议和期刊发表论文近 30 篇，其中以第一作者或通讯作者发表论文近 20 篇，相关成果引用近 2000 次。

个人主页: http://jtdong.com/
谷歌学术: https://scholar.google.com/citations?hl=en&user=dEzL5pAAAAAJ', updated_at = CURRENT_TIMESTAMP WHERE username = 'dongjunting';
UPDATE dtlms_user_profiles SET introduction = '冯世阳，上海人工智能实验室青年研究员。主要研究方向为通用智能体框架与AI自主科学发现。已在ACL、TGRS等国际顶级会议和期刊发表学术论文10余篇，主导或参与多项开源代码仓建设，项目累计star 3k+。作为主要贡献者研发了面向长周期自主科学发现的智能体系统InternAgent，其开源子系统MLEvolve在OpenAI MLE-bench上超越谷歌、微软等机构，取得榜单第一；参与书生科学发现平台Intern-Discovery建设，相关成果被央视、新华网、人民网等多家权威媒体报道。个人主页：https://github.com/Shiyang980713
电子邮箱：fengshiyang@pjlab.org.cn', phone_number = '13388899999', email = 'fengshiyang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'fengshiyang';
UPDATE dtlms_users SET phone_number = '13388899999', email = 'fengshiyang@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'fengshiyang' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '付蓉作为"书生·天际"核心成员，她带领团队通过软硬件协同优化实现系统级加速，成果应用于天际1.0~3.0、桃源平台、万卡混训及AI4S等项目。主导的HPC量子霸权任务获实验室奥斯卡"创新"个人奖，联合多家单位以千卡并行超越谷歌，首次驳斥其"悬铃木"宣称。成果发表于National Science Review及SC等CCF A类顶会，完成多款国产芯片适配。在SC、CVPR等顶会及TSP等国际顶刊累计发表11篇论文，获上海东方英才计划拔尖项目及国家授权专利1项。个人主页:scholar.google.com   EMAIL：furong@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'furong';
UPDATE dtlms_user_profiles SET introduction = '桂韬，复旦大学副研究员，国家级青年人才。研究领域为预训练模型、类人对齐和智能体交互。在高水平国际学术期刊和会议上发表了50余篇论文，曾获钱伟长中文信息处理科学技术奖一等奖、NeurIPS2023大模型对齐 Track最佳论文奖、第七届“中国科协青年人才托举工程”、上海市启明星计划。邮箱：tgui@fudan.edu.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'guitao';
UPDATE dtlms_user_profiles SET introduction = '何哲陟，上海交通大学计算机科学与工程系长聘教轨副教授，上海人工智能实验室双聘副研究员，上海市海外领军人才计划，CCF-A 类期刊 IEEE TCAD 副编辑。长期致力于类脑智能计算软硬件全栈协同设计，研究覆盖类脑大模型算法创新、面向脉冲神经网络的系统软件与高能效硬件全栈设计。已在 Nature Communications、ISCA、MICRO、ASPLOS、HPCA、DAC、TPAMI、ICML 等顶级期刊与会议发表论文 100 余篇，Google Scholar 引用 5000 余次；曾获 DAC 2025、ICCD 2023 最佳论文提名及 DATE 2022 最佳论文奖等多项荣誉。诚邀在类脑大模型算法架构、系统软件或类脑专用硬件任一方向具备扎实基础与浓厚兴趣的同学加入课题组，期待与同学们一道在新一代高能效智能计算前沿共同攻关。
邮箱：zhezhi.he@sjtu.edu.cn Google Scholar：https://scholar.google.com/citations?user=QzDf7GoAAAAJ 课题组主页：https://elliothe.github.io/', updated_at = CURRENT_TIMESTAMP WHERE username = 'hezhezhi';
UPDATE dtlms_user_profiles SET introduction = '侯杰，浦江国家实验室高级工程师。研究方向为超大规模机器学习系统、分布式计算与高性能计算，擅长算法、系统、硬件的端到端协同设计与优化。曾在阿里巴巴、拼多多等互联网公司主导大规模推荐系统与训练平台的构建落地；后于昆仑芯负责分布式异构计算训练系统研发。主要研究兴趣为Agent Infra与下一代超智融合算力体系建设。
邮箱：houjie@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'houjie';
UPDATE dtlms_user_profiles SET introduction = '姜申飞，现任科研任务部前沿探索中心大芯片系统集成团队负责人。2007年毕业于上海交通大学微电子学与固体电子学专业。曾担任芯盟科技有限公司技术副总裁、芯驰科技SOC设计总监、中国科学院通用芯片与基础软件研究中心CPU高速电路部门负责人、 AMD 超威半导体视频IP集成leader等职。具有晶圆级芯片全流程工程经验、3D IC开发和设计、流片经验，具有14nm、7nm高性能大算力AI SOC设计、流片经验，有多款GPU、CPU产品的量产经验。作为”重大项目“晶圆级 AI 芯片架构研究”课题负责人，目前从事高算力人工智能芯片设计、先进封装设计、垂直供电、散热等系统集成工作。', updated_at = CURRENT_TIMESTAMP WHERE username = 'jiangshenfei';
UPDATE dtlms_user_profiles SET introduction = '金海现任华中科技大学教授, 长期从事并行与分布式系统研究，在大规模分布式系统的资源管理、拓扑互联，以及高性能并行系统的领域定制方面做出了重要贡献。主持两项国家973计划项目等重要科研任务；发表IEEE/ACM期刊和重要国际学术会议论文220篇，谷歌学术H-index 82，总引用31000余次；获国际发明专利28项。研发了以热部署和热迁移为核心的分布式系统资源管理方法、网间协作和树网结合的分布式系统拓扑组织机制、基于数据流模式的并行系统领域定制化设计理论与方法等创造性成果。 担任中国计算机学会副理事长、国际IEEE计算机学会会士评审委员会副主席。以第一完成人获国家自然科学二等奖1项、国家科技进步等奖2项。
邮箱:jinhai@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'jinhai';
UPDATE dtlms_user_profiles SET introduction = '李杰岚，上海人工智能实验室青年科学家，主要研究方向为材料高性能计算模拟、几何深度学习、材料生成模型以及大模型和Agent在材料领域的下游应用。毕业于中国科学技术大学，从事PWDFT KSSOLV和DGDFT等高性能材料模拟软件开发。2023年加入微软研究院担任研究员，从事AI for Science的研究工作，负责材料原子基座模型的开发和应用。2025年7月起在上海人工智能实验室工作，致力于通过人工智能推动化学与材料体系的模拟、设计与合成。Google Scholar: https://scholar.google.com/citations?user=SwAzXNEAAAAJ&hl=zh-CN&oi=ao
邮箱:lijielan@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'lijielan';
UPDATE dtlms_user_profiles SET introduction = '李恺林
Email：likailinsjtu@gmail.com
Google Scholar：https://scholar.google.com/citations?user=zEDPB2MAAAAJ&hl=en
Website：https://kailinli.top
李恺林现任上海人工智能实验室物理智能中心青年研究员，上海交通大学博士，师从卢策吾教授。长期从事具身智能中的交互感知、动作生成与机器人运动控制研究，致力于构建从真实物理交互数据到机器人通用操作能力的闭环方法体系，覆盖交互知识建模、仿真强化学习、技能迁移、多本体控制与真机部署。当前重点围绕灵巧手精细操作与人形机器人移动操作，推进底层运控基础模型和高层 WAM/VLA 操作模型协同发展，研究复杂接触、工具使用、全身协调、力位混合控制及跨本体泛化。相关成果发表于 IEEE TPAMI、NeurIPS、CVPR、ICCV 等高水平期刊会议10余篇，并参与 ICCV、ECCV 等国际会议 Workshop、竞赛组织及学术审稿工作。', updated_at = CURRENT_TIMESTAMP WHERE username = 'likailin';
UPDATE dtlms_user_profiles SET introduction = '李力骏，上海人工智能实验室青年研究员，入选东方英才计划。聚焦LLM、MLLM与Agent 的安全、对齐与强化学习，致力于构建可信、安全、可控的新一代智能系统。曾在百度 IDL、腾讯 AI Lab、阿里巴巴达摩院等机构开展 AI 研究工作。近两年来在 ACL、ICML、ICLR、CVPR、EMNLP、AAAI等会议发表20余篇论文，相关工作获 ACL Outstanding Paper，Oral等。欢迎对 Safe AI、LLM/MLLM/Agent安全与对齐感兴趣的同学加入，共同探索前沿问题。
邮箱：lilijun@pjlab.org.cn
主页：https://adwardlee.github.io/', phone_number = '17788889999', email = 'lilijun@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'lilijun';
UPDATE dtlms_users SET phone_number = '17788889999', email = 'lilijun@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'lilijun' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '林洲汉，上海交通大学人工智能学院副教授、上海人工智能实验室双聘导师，John Hopcroft计算机科学中心副主任，国家海外高层次青年人才。博士师从于深度学习领域图灵奖得主Yoshua Bengio。目前主要从事自监督学习、语言模型新架构和预训练。代表作有Memory Decoder、Next-Concept-Prediction、PonderLM、FlowRL、以及self-attention雏形。谷歌学术总引用量12000余次，担任ICLR、ICML、NeurIPS、ACL、EMNLP、AAAI等会议的领域主席。
邮箱：hantek@sjtu.edu.cn、个人主页：hantek.github.io、Google Scholar主页：https://scholar.google.com/citations?user=LNZ4efwAAAAJ', updated_at = CURRENT_TIMESTAMP WHERE username = 'linzhouhan';
UPDATE dtlms_user_profiles SET introduction = '球系统是我们赖以生存的复杂巨系统，具备可检验的预测体系与紧迫的真实业务需求。它不仅可应用于气候变化、资源勘探及灾害预警，更是AI时代构建世界模型与验证科学发现能力的天然试验场。 团队长期深耕 AI for Earth Science，推出了“风乌”、Earth-o1 等基础模型，并研发了科学智能发现系统 EarthLink。核心科研成果发表于 Nature 子刊、Science 子刊及 NeurIPS 等顶会顶刊，更实现业务化运行与商业落地转化。 欢迎有志同学加入我们：lingfenghua@pjlab.org.cn。', updated_at = CURRENT_TIMESTAMP WHERE username = 'lingfenghua';
UPDATE dtlms_user_profiles SET introduction = '刘东瑞现任上海人工智能实验室青年科学家，聚焦智能体安全和可解释性 (小红书实名)。
主导智能体评测诊断套件AgentDoG，开源工作Github星标数2w+，全网下载量1w+，已应用于腾讯，阿里等公司。负责SafeWork-R1安全高效推理和SafeWork-F1&1.5，获Anthropic 联合创始人解读，并受邀为DeepMind 分享。发表论文40余篇，涵盖CVPR 2024 最佳论文候选奖，ACL 2025杰出论文奖, 多篇ICLR，CVPR，ACL，AAAI Oral，担任NeurIPs和ICLR领域主席。
电子邮箱：liudongrui@pjlab.org.cn
个人主页：https://shenqildr.github.io/', updated_at = CURRENT_TIMESTAMP WHERE username = 'liudongrui';
UPDATE dtlms_user_profiles SET introduction = '研究方向融合脑科学/神经科学与人工智能，聚焦一个核心问题：如何让AI启发脑研究，又如何让脑机理点亮新AI？
一方面，我致力于“用神经网络研究神经网络”——借助基础模型、智能体、数字孪生、具身智能等前沿工具，建立类脑计算模型，解析生物神经网络的信息处理机制与复杂行为生成逻辑，并将这些从大脑中“逆向解析”出的计算原理，反哺下一代AI架构的设计。
另一方面，我和顶级医疗机构开展神经与精神疾病的临床实践，重点围绕阿尔茨海默病、抑郁、偏瘫、脑肿瘤等疾病的诊疗困境，发展更精准、可解释的诊断与智能调控方法，实现从脑机制解析到临床干预的闭环。
一句话概括：理解大脑如何工作，构建受大脑启发的人工智能，并用它们来修复大脑。
邮箱liumianxin@pjlab.org.cn。个人主页https://scholar.google.com/citations?user=LplimusAAAAJ&hl=en', updated_at = CURRENT_TIMESTAMP WHERE username = 'liumianshen';
UPDATE dtlms_user_profiles SET introduction = '弼卿，上海人工智能实验室星启青年研究员，中国工程院技术专班与国家供应链平台建设委员。主要从事模型架构与学习方法及其在科学领域的交叉应用。在NeurIPS、CVPR、ACL、TPAMI等发表论文60余篇。创新设计通专动态架构Nirvana，赋能软硬协同与脑卒中早筛；自研业界首款块扩散语言模型SDAR，推理速度突破6600tgs,月均下载5万+；搭建多智能体系统MARTI，实现计算化学领域Nature级自主科学突破。研究成果获人民日报等主流媒体报道，多项技术落地腾讯、华为、天坛医院等机构。主持四项国家、省部级重大课题及国家自然科学基金项目。
邮箱：qibiqing@pjab.org.cn | qibiqing7@gmail.com | qibiqing@hku.hk
个人主页：https://biqing-qi.github.io/', updated_at = CURRENT_TIMESTAMP WHERE username = 'qibiqing';
UPDATE dtlms_user_profiles SET introduction = '钱建民博士现任上海人工智能实验室高级工程师，负责了deeplink大规模混训混推相关技术构建与交付，参与了面向超大规模MOE模型训练框架Xtuner的研发工作。在实验室内部负责了大规模（千卡规模）推理服务平台的构建和性能优化，主导了LightRFT强化学习框架的开源工作。曾经在华为2012实验室分布式并行实验室从事大规模分布式系统研究，参与华为serverless平台的构建，相关成果上线华为云并发表在Sigcomm2024。博士期间主要从事操作系统和分布式系统的研究，主要成果发表在Infocomm，ICCD和DATE等会议上。邮箱：qianjianmin@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'qianjianmin';
UPDATE dtlms_user_profiles SET introduction = '师从悉尼大学MMLab欧阳万里教授。致力于基因组学与多组学的AI基础能力研究与应用。在Nature子刊、 NeurIPS、ICML和 CVPR等人工智能顶级期刊和会议发表论文20余篇。于浦江实验室承担基因组学的高峰孵化项目，入选浦江创新论坛2025十大科学进展。希望与志同道合的同学一起，打造连续的高影响力的AI for Biology工作，从底层算法架构的创新，到基于全球级别的基因组学与多组学大数据打造基座模型与Agent；从理解生命法则，到定向设计蛋白质与基因组序列，为真实世界的调控机制、细胞命运、生命健康与神经、肿瘤学难题提供新解法。你将拥有充足的算力和广阔的探索空间，加入我们，一起去征服 AI for Biology 的星辰大海！
邮箱：renyuchen@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'renyuchen';
UPDATE dtlms_user_profiles SET introduction = 'https://intersun.github.io/
My research focuses on AI for Science and LLMs for Scientific Discovery. I am primarily interested in developing foundational generative models for biomolecular structure prediction/design, proteomics and AIVC, while also expanding into Agentic Science for autonomous scientific reasoning.
Previously, I was a Researcher on the Knowledge and Language Team at Microsoft Research, working with JJ Liu and Jianfeng Gao. I received my PhD from TTI-Chicago, a philanthropically endowed computer science research institute in the University of Chicago, advised by Prof. Jinbo Xu. Prior to that, I received my B.S. degree from the School of Mathematics at Fudan University.
EMAIL:siqisun@fudan.edu.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'sunsiqi';
UPDATE dtlms_user_profiles SET introduction = '孙友邦，浦江国家实验室一类双聘助理研究员，清华大学电子工程系助理研究员。主要研究方向为大语言模型推理技术、例如强化学习，多智能体与优化等领域的理论以及在大语言模型中的应用、人工智能安全等。已发表一作学术论文十余篇，包含NeurIPS，ICLR，ICML，IEEE TAC等人工智能和控制理论领域顶级会议与期刊。根据谷歌学术搜索，申请人的累计被引用量超过1000次。同时，这些研究成果支撑了多个开源项目的开发，合计获得Github星标超过六千次。

https://scholar.google.com/citations?user=gCToDVQAAAAJ&hl=en
https://sundave1998.github.io/', updated_at = CURRENT_TIMESTAMP WHERE username = 'sunyoubang';
UPDATE dtlms_user_profiles SET introduction = '汪汗青博士，上海人工智能实验室物理智能中心青年科学家，数字模拟平台团队负责人，主要研究方向为具身仿真与评测。博士毕业于北京理工大学，曾于微软亚洲研究院、阿联酋起源人工智能研究院、苏黎世联邦理工学院访问。他以第一作者在CVPR、ECCV、ICCV、NeurIPS、TPAMI、IJCV等计算机视觉和人工智能的顶会顶刊发表论文十余篇，并多次担任相关会议期刊的审稿人。他曾获上海市超级博士后、东方英才计划拔尖项目等荣誉。他作为主要负责人带领实验室团队研发了通用具身仿真平台桃源(InternUtopia)，目前已在开源社区Github上获得1.2k+ star。
Github: https://github.com/HanqingWangAI
个人主页：https://hanqingwangai.github.io/
邮箱：hanqingwang.c@gmail.com', updated_at = CURRENT_TIMESTAMP WHERE username = 'wanghanqing';
UPDATE dtlms_user_profiles SET introduction = '汪旭鸿，博士毕业于SJTU，美国UC伯克利访问学者，曾荣获研究生国家奖学金（两次）。在包括Nature Machine Intelligence、ICLR、ACL等共发表 40 余篇论文，单篇最高引用260，H指数15。曾深度参与蚂蚁图计算系统研发以及开源图深度学习框架DGL(1.5万星)建设。研究兴趣为探索安全可信的scaling law，目前主要从事下一代可信训练infra研究，开源了首个支持多基模共同博弈对抗训练的RL框架SAfactory。

个人主页：https://wangxuhongcn.github.io/
邮箱: wangxuhong@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangxuhong';
UPDATE dtlms_user_profiles SET introduction = '王栋，上海人工智能实验室青年研究员，聚焦于研发大规模真机异构数据贯通的具身操作基座模型，代表性研究成果Spatial-VLA，EO-1具身基座大模型预训练与后训练，实现了异构具身机器人的泛化复杂操作，模型性能超过Google RT系列，Physical Intelligence，NVIDIA等前沿企业科研机构的水平，取得2025年度Behavior-1K具身操作挑战赛全球第二名的成绩，受到Google DeepMind，NVIDIA，Huggingface Lerobot等国际顶尖企业关注并合作，取得了前沿的国际影响力。联系邮箱：wangdong@pjlab.org.cn, 谷歌学术：https://scholar.google.com/citations?user=dasL9V4AAAAJ。', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangdong';
UPDATE dtlms_user_profiles SET introduction = '王翰竟现任上海人工智能实验室青年研究员，研究方向为智能体框架以及多智能体强化学习系统；参与前沿模型架构探索的训推系统框架支持工作、DeepLink 开放计算生态以及超节点生态工作。研究成果发表于 JMLR、ICML、HPDC等机器学习或分布式计算领域国际顶级学术会议和期刊。 
电子邮箱：wanghanjing@pjlab.org.cn
Google Scholar: https://scholar.google.com/citations?user=_tpkhMcAAAAJ&hl=en', updated_at = CURRENT_TIMESTAMP WHERE username = 'wanghanjing';
UPDATE dtlms_user_profiles SET introduction = '上海人工智能实验室青年科学家，专注晶圆级芯片及系统，通过架构工艺协同创新构建AI计算基础设施。曾任职博通、紫光、阿里等头部企业，交付数款国际领先芯片。第一发明人获多项专利。邮箱:wanglei@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'wanglei';
UPDATE dtlms_user_profiles SET introduction = '王翔，中国科学技术大学特任教授、博导，国家级青年人才。研究方向包括大模型与智能体及安全可信，谷歌学术总引用3.8万余次，2篇论文进入国际顶会SIGIR近十年引用量最高与次高序列，并被斯坦福等国际知名高校课程与教材采用。获人工智能顶会ICLR最佳论文奖、中国人工智能学会吴文俊人工智能自然科学一等奖、SIGIR杰出青年奖、MIT-TR35、国际基础科学大会前沿科学奖、浦江青年学者等，入选AI 2000全球人工智能智能最具影响力学者榜单，并在“信息检索与推荐”领域排名第三。主持基金委重点项目、面上项目、重大研究计划培育项目与重大专项课题。担任TPAMI、TOIS等国际顶刊的Associate Editor。

邮箱：xiangwang@ustc.edu.cn
个人主页：https://xiangwang1223.github.io/
Google Scholar：https://scholar.google.com.sg/citations?user=HdhaQB0AAAAJ&hl=en', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangxiang';
UPDATE dtlms_user_profiles SET introduction = 'Postdoc@UCLA (Prof. Kai-Wei Chang)，CS PhD@Columbia University (Prof. Shih-fu Chang, 美国工程院院士) 。他参与多个DARPA项目，担任ECOLE和MCS项目的主要贡献者。他领导了与顶尖机构的协作，取得了多个知名基准数据集的SOTA。此外，他还带领团队，在微软全球百万名人人脸识别MS-Celeb-1M挑战赛以及DARPA机器常识推理排行榜上取得了第一名。他作为共同负责人Co-PI荣获得了Google Research Scholar Program Award，也曾在Google DeepMind的核心Gemini大模型团队合作工作了两年，也在Microsoft Research的多模态组合作工作了一年。他曾作为前10号员工，在小鹏汽车的AI研究院全职深度贡献。迄今为止，他已发表19篇顶级会议论文（10篇为第一或共一）和7篇研讨会论文。其中Oral口头汇报6次，Spotlight高光1次。他著有8项AI相关授权专利（7 U.S. 和1 China），他的研究工作在Google Scholar被引用超过1400多次，累积i10-index为19。他的研究成果曾被PaperWeekly、 AI2、DARPA、新智源和量子位等广泛报道。
Personal Website: zhecanwang.com
Google Scholar ID: uqhpnmgaaaaj 
GitHub: github.com/zhecanjameswang
Patent: patents.justia.com/inventor/zhecan-wang
Linkedin: https://www.linkedin.com/in/jameszhecanwang/', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangzhecan';
UPDATE dtlms_user_profiles SET introduction = '王尊，上海人工智能实验室青年科学家，清华大学2017级物理学博士。研究方向为大语言模型、智能体、强化学习等方向。负责书生·浦语 Intern S1-Pro、Intern-S2 Preview 等模型 Agent 能力方向的后训练技术体系研发与交付，涵盖 Function Calling、Deep Search、GUI Agent、Code Agent 等关键场景，相关模型综合性能达到开源社区领先水平。2022年博士毕业后任微软亚洲研究院 Senior Researcher，期间获 OGB Large-scale Challenge@NeurIPS 2022 (PCQM4Mv2) 第二名。在 Nature 系列正刊以及子刊、 AI 顶级会议发表论文30余篇，Google Scholar 引用2400余次，h-index 14。
欢迎对大模型、智能体与强化学习感兴趣的同学加入团队。
联系方式：
 邮箱：wangzun1@pjlab.org.cn
 GitHub：Zun-Wang - Overview
 Google Scholar：https://scholar.google.com/citations?user=6MTUgHcAAAAJ', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangzun';
UPDATE dtlms_user_profiles SET introduction = '吴烜圣老师现任上海人工智能实验室青年研究员，研究聚焦大模型隐空间表征与细粒度可控性，以 "实用解释性" （UsableXAI）理念解决指令跟随、幻觉检测、数学推理、AI 安全等工业界核心问题。团队成果获 ICML 2026 Spotlight、Huggingface 周榜第一，多篇顶会 Oral 论文，参与千万美元级课题。关于吴老师的更多信息请参阅 https://jacksonwuxs.github.io/。欢迎对大模型内部机理感兴趣的同学加入，请发送简历到 wuxuansheng@pjlab.org.cn，并在简历正文用一句话总结自己的亮点！', updated_at = CURRENT_TIMESTAMP WHERE username = 'wuxuansheng';
UPDATE dtlms_user_profiles SET introduction = '若你拒绝被单一赛道定义，这里或许有另一种可能。徐甲课题组聚焦前沿AI风险管理与AI安全规约技术体系，探索自进化智能体评估与环境搭建，贯通数学建模、社会哲学与公共治理。对话联合国、卡内基及头部企业，连接政府、高校、投资人与国际组织。十余篇SCI、SafeWork-F1与大设施架构是研究支撑。尊重个体差异，支持学术、产业与政策等多维目标。期待你的加入。
电子邮箱:xujia@pjlab.org.cn', phone_number = '17788889999', email = 'xujia@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'xujia';
UPDATE dtlms_users SET phone_number = '17788889999', email = 'xujia@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'xujia' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '徐兴成，北京大学与牛津大学联合培养博士，现任上海人工智能实验室研究员，入选东方英才计划拔尖项目、启明星项目，相关研究成果获MIT科技评论、机器之心、深科技等媒体关注报道。研究聚焦人工智能基础理论、智能体系统、智能体安全与自进化，目前围绕大模型强化学习训练、智能体Harness工程与安全体系建设开展研究，致力于构建能够持续进化、安全可信的新一代智能体。欢迎富有创造力、勇于探索的青年学子加入，探索智能时代最具挑战性的前沿问题。
邮箱：xuxingcheng@pjlab.org.cn
个人主页：https://xingchengxu.github.io/', updated_at = CURRENT_TIMESTAMP WHERE username = 'xuxingcheng';
UPDATE dtlms_user_profiles SET introduction = '徐旭东，本科毕业于南京大学自动化专业，排名第一；博士毕业于香港中文大学信息工程系，师从林达华教授。博士期间在Meta Reality Labs实习，从事元宇宙相关研究。现任上海AI Lab物理智能中心的研究员，曾荣获上海市BYL人才计划。

研究方向聚焦于具身智能中的可交互世界模拟器（Interactive world simulator），涵盖可交互三维场景生成（Interactive 3D Scene Generation）与第一视角的世界模型（Egocentric World Models）两大方向，分别探索基于 3D 和基于视频的方案。代表成果包括 EgoSim、RoboVIP、Code-as-Room、MesaTask、AnySplat 等，成果发表于 NeurIPS、ECCV、SIGGRAPH Asia等顶级会议/期刊。

Google scholar: https://scholar.google.com.hk/citations?hl=en&user=D8VMkA8AAAAJ
Email: xuxudong@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'xuxudong';
UPDATE dtlms_user_profiles SET introduction = '国家杰青基金获得者，上海高校特聘教授（东方学者），现任电信学院副院长、图像通信所副所长。主要研究视频编码与通信、图像处理与模式识别、视频分析与检索。发表SCI 收录论文60 篇（IEEE Trans30 篇）。申请发明专利35项（授权14项），国际发明专利7项。主持973及863课题、国家自然科学基金重点等国家级科研项目10项。获上海市科技进步一等奖（第一完成人）、上海青年科技英才、德国洪堡基金、微软青年教授奖、SPIE青年科学家奖、教育部新世纪优秀人才计划。IEEE Signal Processing Letters编委、Springer CCIS领域编委、Digital Signal Processing (Elsveier Press) 编委，IEEE视觉信号处理与通信技术委员会、信号处理系统设计与实现技术委员会委员，IEEE高级会员，IEEE SiPS2007及IEEE BMSB-3DTV2010大会程序主席。
    xkyang@sjtu.edu.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'yangxiaokang';
UPDATE dtlms_user_profiles SET introduction = '叶南阳，上海交通大学长聘教轨副教授，剑桥大学博士。长期聚焦深度神经网络泛化理论与方法研究，核心致力于提升大模型与具身智能系统的分布外泛化性能。研究围绕视觉语言大模型、具身智能展开，从理论与算法层面突破泛化瓶颈，推动AI系统在未知场景中可靠决策。主持国家自然科学基金等项目，入选上海海外高层次人才，成果发表于ICML，ICLR，NeurIPS，CVPR，T-PAMI，IJCV等顶会顶刊。联系邮箱 ynylincoln@sjtu.edu.cn。', updated_at = CURRENT_TIMESTAMP WHERE username = 'yenanyang';
UPDATE dtlms_user_profiles SET introduction = '于沐霖现任上海人工智能实验室物理智能中心研究员，国家自然科学基金青C项目获得者，2022年获INRIA博士学位。主要研究方向包括三维视觉、世界模型、神经渲染与三维重建，关注三维空间表征、场景理解与交互预测等基础问题，探索相关技术在具身智能感知、推理与操作中的应用。相关成果发表于CVPR、NeurIPS、ICLR、TPAMI、ACM TOG等国际会议和期刊，并作为核心成员参与LandMark/书生·天际及DigitalBuddy等项目。
yumulin@pjlab.org.cn
https://mulinyu.github.io/', updated_at = CURRENT_TIMESTAMP WHERE username = 'yumulin';
UPDATE dtlms_user_profiles SET introduction = '于天舒，香港中文大学（深圳）助理教授+上海AI Lab双聘研究员。团队围绕面向化学/化工的人工智能，开展从基础理论、算法模型到系统落地的AI全链条研究。我们关注图论、PDE、分子与反应表征、可控生成、逆合成规划、实验决策与过程优化，挑战数据稀缺、机理复杂、约束强和搜索空间巨大的核心难题，目标是构建可信、高效、可用的AI化学家，加速新分子、新反应与新工艺发现。对科研鼓励长期主义+重要问题驱动。欢迎联系yutianshu@cuhk.edu.cn，或者访问https://mypage.cuhk.edu.cn/academics/yutianshu/。', updated_at = CURRENT_TIMESTAMP WHERE username = 'yutianshu';
UPDATE dtlms_user_profiles SET introduction = '臧宇航博士毕业于新加坡南洋理工大学，现任上海人工智能实验室青年研究员，研究方向为多模态大模型，负责书生科学大模型多模态感知专项能力提升。论文 Visual-RFT 入选 PaperDigest ICCV 2025 Top-10 最具影响力论文。已在 ICML/ICLR/NeurIPS/CVPR 等会议与期刊发表论文 50 余篇，谷歌学术引用 10100+。担任 CVPR 2026、ICLR 2026、NeurIPS 2025、COLM 2026 等学术会议领域主席以及 TMLR 期刊执行编辑。
个人主页: https://yuhangzang.github.io/
谷歌学术: https://scholar.google.com/citations?user=hW23VKIAAAAJ
如果你对 agentic post-training、spatial understanding 等多模态方向有兴趣，欢迎邮件与我联系，联系邮箱: zangyuhang@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'zangyuhang';
UPDATE dtlms_user_profiles SET introduction = '张岸，中国科学技术大学特任教授、博导，国家级青年人才，Alpha Lab 负责人，Web领域女性新星奖。
如果你想让大模型不止会回答，而是更会思考、更会提出问题、更会持续进化；如果你想成为AI时代的弄潮人，度过快乐的硕博生涯，加入我们，一起做有趣、有价值、有影响力的研究。
主页：https://anzhang314.github.io/
邮箱：An_Zhang@ustc.edu.cn
Google Scholar: https://scholar.google.com.sg/citations?user=BcX7GJcAAAAJ&hl=en', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangan';
UPDATE dtlms_user_profiles SET introduction = '张鸿杰博士毕业于南京大学计算机科学与技术系，入选2022年上海市启明星杨帆人才专项和2025年上海市东方英才青年项目，主要研究方向是多模态理解生成一体化模型（InternVL-U系列）和矢量多模态大模型（InternSVG系列），负责科学大模型（InternS系列）的研发。团队氛围融洽，在顶级学术会议和期刊上中稿率高。
电话：19121871912
邮箱：nju.zhanghongjie@gmail.com
Google Scholar: https://scholar.google.com/citations?user=Zl_2sZYAAAAJ&hl=zh-TW', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhanghongjie';
UPDATE dtlms_user_profiles SET introduction = '张乔生，上海AI Lab青年科学家，上交/复旦兼职博导。于香港中文大学获得学士与博士学位，曾在新加坡国立大学、佐治亚理工学院从事科研工作。主要关注强化学习、安全可信大模型、信息论与AI基础理论研究。在理论层面解决了强化学习、无监督学习领域多个基础难题，在应用层面联合牵头研发了多模态推理模型MM-Eureka、安全可信大模型SafeWork-R1等。研究成果获香农奖得主、ACM/IEEE Fellow等知名学者以及MIT/Stanford/Princeton/Berkeley/Google/Nvidia等机构引用与积极评价。入选国家级青年人才计划与上海市海外高层次人才计划。
邮箱 zhangqiaosheng@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangqiaosheng';
UPDATE dtlms_user_profiles SET introduction = '上海人工智能实验室青年科学家，目前主要方向是科学发现智能体系统harness设计，知识演绎与推理方法研究，智能体进化与训练以及在物质科学方面的应用。以通讯作者发表多篇nature science子刊论文。组里的学生发表nature science级别论文机会非常多，合作机会也非常多。
邮箱：zhangshufei@pjlab.org.cn', phone_number = '13388899999', email = 'zhangshufei@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangshufei';
UPDATE dtlms_users SET phone_number = '13388899999', email = 'zhangshufei@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangshufei' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '张文涛，北京大学国际机器学习研究中心研究员、博士生导师。曾任职于腾讯、Apple AIML 和加拿大Mila。研究聚焦Data-Centric AI、LLM数据系统、数据治理智能体与AI4Science。近五年一作/通讯CCF-A论文100+篇，谷歌学术引用14,000+次，入选Elsevier全球前2%科学家，2026 CSRanking北大AI/ML及AI+Data方向首位，3次获顶会最佳论文奖。主持基金委、科技部、教育部、北京市科委及校企合作科研项目 20 余项。曾获中国电子学会科技进步一等奖，入选智源学者、浦江青年学者、ACM SIGMOD China 新星奖等。开源DataFlow、MinerU、Angel等获GitHub Star超7万。
邮箱：wentao.zhang@pku.edu.cn
个人主页：https://zwt233.github.io/
Google Scholar：https://scholar.google.com/citations?user=JE4VON0AAAAJ
GitHub：https://github.com/OpenDCAI/', phone_number = '18899996666', email = 'zhangwentao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangwentao';
UPDATE dtlms_users SET phone_number = '18899996666', email = 'zhangwentao@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangwentao' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '张行程，上海人工智能实验室青年科学家。成果方向覆盖国产AI软硬件技术突破与基础设施建设渗透等，率先实现国产自研训练框架高效适配国产硬件平台、分钟级训练、千卡大规模训练，国产万卡异构混训等。打造DeepLink 人工智能开放计算体系，推动训练芯片的标准化建设，包括评测标准、适配标准等工作。拉通多家主流国产芯片厂商进行标准化适配。邮箱:zhangxingcheng@pjlab.org.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhangxingcheng';
UPDATE dtlms_user_profiles SET introduction = '赵振现任青年研究员，主攻多模态科学推理、交叉领域大模型研发，主持重大专项课题，助力AI技术在能源电力领域落地应用。聚焦AI4Science、高效数据感知、科学智能决策，累计发表AI顶会顶刊40余篇，谷歌引用超4000次。
zhaozhen@pjlab.org.cn

http://zhaozhen.me/', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhaozhen';
UPDATE dtlms_user_profiles SET introduction = '我们关注一个很酷的问题：AI 能不能不只是读论文、写代码、聊天，而是真的走进实验室做实验？
周东展博士现任上海人工智能实验室 AI for Science 中心青年科学家，聚焦自主实验室方向，致力于融合大模型、智能体和具身智能技术，让 AI 从数字世界走向物理世界。近期工作包括指导实验操作的智能眼镜、egocentric数据飞轮，以及能够自主完成实验任务的机器人。欢迎对自主实验室感兴趣的同学加入，一起把“会思考的 AI”变成“会动手的 AI”。
zhoudongzhan@pjlab.org.cn
Google Scholar: https://scholar.google.com/citations?user=Ox6SxpoAAAAJ&hl=zh-CN', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhoudongzhan';
UPDATE dtlms_user_profiles SET introduction = '周浩，清华大学智能产业研究院副研究员。他的主要研究方向是大规模语言模型，及其在科学发现中的应用。他曾任字节跳动研究科学家和副总监，领导搭建了字节跳动的文本生成中台和AI辅助药物设计两个方向的研发团队。他长期担任ICML、NeurIPS，ICLR，ACL等人工智能顶级会议的领域主席，在人工智能顶级国际会议上发表论文100余篇。曾获人工智能学会优博，CCF-NLPCC 青年新锐科学家，ACL 2021 最佳论文奖（通讯作者）和北京市科技新星等荣誉。
个人主页：
https://zhouh.github.io/
邮箱地址：
zhouhao@air.tsinghua.edu.cn', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhouhao';
UPDATE dtlms_user_profiles SET introduction = '周杰，上海人工智能实验室双聘，华东师范大学青年研究员，博士生导师。主要研究大模型、自进化相关领域，以一作/通讯作者在CVPR、ICLR、ACM Computing Survey等会议期刊上发表论文50余篇，Google引用3000余次，获得 COLING 2022杰出论文奖、FITEE封面论文，以项目负责人主持国自然面上、上海市经信委AI专项、CIPS-SMP清智大模型基金等科研项目多项。其提出经验驱动终身学习的自进化理念并将其用于教育、农业生态等领域，带领团队研发并开源了技能自进化框架AutoSkill、教育大模型EduChat等产品，在GitHub、Huggingface开源平台下载上万次。曾获得上海市科技进步二等奖、上海市东方英才计划青年项目、上海市启明星扬帆计划等荣誉。
邮箱：jzhou@cs.ecnu.edu.cn
Google学术：https://scholar.google.com/citations?user=dKt8wwQAAAAJ&hl=zh-CN#
Github：ECNU-ICALK', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhoujie';
UPDATE dtlms_user_profiles SET introduction = '周铭博士2023年毕业于上海交通大学，师从张伟楠教授。专注研究强化学习、具身智能及机器学习系统，谷歌学术引用 2400+，曾获CoRL2020最佳系统论文奖，出版《动手学博弈论》，开源项目star > 3k（自动驾驶、多智能体强化学习及多模态大模型）。目前，周铭博士在浦江实验室物理智能中心负责人形机器人原生运控/操作系统、世界模型训练架构及数据基建研发。

邮箱：zhouming@pjlab.org.cn
个人主页：https://www.mingzak.com/
Github：KornbergFresnel - Overview
Google学术：https://scholar.google.com/citations?user=xuW4NIYAAAAJ&hl=en&oi=sra', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhouming';
UPDATE dtlms_user_profiles SET introduction = '周煊赫，现任上海交通大学计算机学院长聘轨助理教授，上海人工智能实验室兼职助理研究员，智源青年学者。主要研究Self-Improving Agent、多模态数据检索、大模型记忆体。在SIGMOD、NIPS、VLDB、ACL、CVPR、TKDE等CCF A类会议和期刊上已发表论文数十篇，包括近五年NIPS、VLDB、ICDE高被引论文，入选卡耐基梅隆大学、康奈尔大学等高校课程。谷歌学术引用量四千余次。曾获 SIGMOD 2025 Jim Gray Honorable Mention（大陆首位）、VLDB 2023 Best Industry Paper Runner-up（第一作者）、CCF优博、世界人工智能大会云帆奖、微软学者、字节跳动奖学金、清华特奖等荣誉。代表性工作OpenMLDB、ByteHouse已在金融、电商、能源等数百个真实场景中实现规模化应用。
电子邮箱:zhouxuanhe@pjlab.org.cn
个人主页：https://db.zhouxh.store', updated_at = CURRENT_TIMESTAMP WHERE username = 'zhouxuanhe';
UPDATE dtlms_user_profiles SET introduction = '王之港，上海人工智能实验室青年科学家。主要研究方向为机器智能感知、具身导航、自主路径规划及异构具身智能体。曾于 2019 年、2020 年两度斩获 AICity 国际人工智能技术挑战赛冠军，在CVPR/ICCV/ECCV/ICLR/AAAI/ICRA/TIP等人工智能顶级会议和期刊发表论文30余篇。团队研发的具身导航项目OpenFly被工信部评为优质开源项目，受邀参展 2025 国际低空经济博览会，已在应急救援、安全巡检等领域实现落地应用。异构具身智能体等项目获得 Asia Times、中国日报、雷锋网等多家国内外主流媒体的关注与报道。
代表性成果github链接：https://shailab-ipec.github.io/openfly/
Google Scholar：https://scholar.google.com/citations?hl=zh-CN&user=cw3EaAYAAAAJ&view_op=list_works
邮箱：wangzhigang@pjlab.org.cn', phone_number = '18729320459', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangzhigang';
UPDATE dtlms_users SET phone_number = '18729320459', updated_at = CURRENT_TIMESTAMP WHERE username = 'wangzhigang' AND is_deleted = FALSE;
UPDATE dtlms_user_profiles SET introduction = '主要研究方向为，生物多模态模型和生物工程算法的开发。解决传统生物工程中低效高成本问题，大幅提高蛋白类生物医药的开发效率。在Science Advances, PNAS, Nature Communications 和NeurIPS 上发表10余篇论文。
E-mail: tpan1039@gmail.com
Google Scholar: https://scholar.google.com/citations?user=rjWJowIAAAAJ&hl=zh-CN', phone_number = '18899996666', email = 'tanpan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'tanpan';
UPDATE dtlms_users SET phone_number = '18899996666', email = 'tanpan@dtlms.local', updated_at = CURRENT_TIMESTAMP WHERE username = 'tanpan' AND is_deleted = FALSE;

COMMIT;
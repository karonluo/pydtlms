# dtlms_portal_application_english_proficiencies 主备库比对报表

- 生成时间：2026-06-13 15:48:02
- 主库：test061301
- 备库：test0604
- 比对表：dtlms_portal_application_english_proficiencies

## 汇总

| 指标 | 数值 |
| --- | ---: |
| candidate_no 仅在主库存在 | 1030 |
| candidate_no 仅在备库存在 | 0 |
| candidate_no 在两边完全一致 | 920 |
| candidate_no 在两边存在差异 | 3 |
| 仅附件 URL 不一致的 candidate_no | 181 |
| 主库多余行数 | 1055 |
| 备库多余行数 | 3 |

## 差异明细

### candidate_no = SH20270003

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1849` `application_id=31` `exam_name=CET-6` `score_text=593` `certificate_attachment_url=/api/v1/portal/attachments/student-188/english_certificate/english_certificate-fe8864db14734925ae11f77597af56c9.pdf` | `id=4` `application_id=31` `exam_name=CET-6` `score_text=593` `certificate_attachment_url=/portal-attachments/uploads/student-188/english_certificate/english_certificate-fe8864db14734925ae11f77597af56c9.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270004

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1788` `application_id=32` `exam_name=CET-6` `score_text=500` `certificate_attachment_url=/api/v1/portal/attachments/student-290/english_certificate/english_certificate-bc849c671396496daf6cb3c1c8c3888e.png` | `id=5` `application_id=32` `exam_name=CET-6` `score_text=500` `certificate_attachment_url=/portal-attachments/uploads/student-290/english_certificate/english_certificate-bc849c671396496daf6cb3c1c8c3888e.png` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270008

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1733` `application_id=36` `exam_name=CET-6` `score_text=545` `certificate_attachment_url=/api/v1/portal/attachments/student-392/english_certificate/english_certificate-68d60dfe464d42768de2fd119c14dacd.pdf` | `id=10` `application_id=36` `exam_name=CET-6` `score_text=545` `certificate_attachment_url=/api/v1/portal/attachments/student-392/english_certificate/english_certificate-bb1a614a659f4fa7b4be7722b40550a9.pdf` |
| 第 2 行 | `id=1986` `application_id=36` `exam_name=其他` `score_text=650` `certificate_attachment_url=/api/v1/portal/attachments/student-392/english_certificate/english_certificate-68d60dfe464d42768de2fd119c14dacd.pdf` | `id=11` `application_id=36` `exam_name=其他` `score_text=650` `certificate_attachment_url=/api/v1/portal/attachments/student-392/english_certificate/english_certificate-68d60dfe464d42768de2fd119c14dacd.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270019

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1760` `application_id=47` `exam_name=CET-6` `score_text=510` `certificate_attachment_url=/api/v1/portal/attachments/student-343/english_certificate/english_certificate-56b62a10a786409a8704f4f810c5628d.pdf` | `id=22` `application_id=47` `exam_name=CET-6` `score_text=510` `certificate_attachment_url=/api/v1/portal/attachments/student-343/english_certificate/english_certificate-0d07c3c5dec840c4999f3b024b8e89c3.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270020

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1708` `application_id=48` `exam_name=CET-6` `score_text=615` `certificate_attachment_url=/api/v1/portal/attachments/student-430/english_certificate/english_certificate-2e66531fe63d475cb1b35a7c82bb3652.pdf` | `id=23` `application_id=48` `exam_name=CET-6` `score_text=615` `certificate_attachment_url=/api/v1/portal/attachments/student-430/english_certificate/english_certificate-5dfbf87b5a9c4e39a4508300cdcf2200.pdf` |
| 第 2 行 | `id=1987` `application_id=48` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-430/english_certificate/english_certificate-2e66531fe63d475cb1b35a7c82bb3652.pdf` | `id=24` `application_id=48` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-430/english_certificate/english_certificate-2e66531fe63d475cb1b35a7c82bb3652.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270022

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1793` `application_id=51` `exam_name=IELTS` `score_text=8` `certificate_attachment_url=/api/v1/portal/attachments/student-281/english_certificate/english_certificate-6976740bcc0a4e189b9cf008f9ee3670.pdf` | `id=26` `application_id=51` `exam_name=IELTS` `score_text=8` `certificate_attachment_url=/api/v1/portal/attachments/student-281/english_certificate/english_certificate-50f79b864fa34170a2b07af5d731191d.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270030

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1777` `application_id=59` `exam_name=CET-6` `score_text=528` `certificate_attachment_url=/api/v1/portal/attachments/student-315/english_certificate/english_certificate-e50bc7a78dce4142b062ed3dc3b497e7.pdf` | `id=34` `application_id=59` `exam_name=CET-6` `score_text=528` `certificate_attachment_url=/api/v1/portal/attachments/student-315/english_certificate/english_certificate-93f20b82c21a4354a0cbab2ee576fc8d.pdf` |
| 第 2 行 | `id=1988` `application_id=59` `exam_name=其他` `score_text=552` `certificate_attachment_url=/api/v1/portal/attachments/student-315/english_certificate/english_certificate-e50bc7a78dce4142b062ed3dc3b497e7.pdf` | `id=35` `application_id=59` `exam_name=其他` `score_text=552` `certificate_attachment_url=/api/v1/portal/attachments/student-315/english_certificate/english_certificate-e50bc7a78dce4142b062ed3dc3b497e7.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270040

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1700` `application_id=70` `exam_name=CET-6` `score_text=599` `certificate_attachment_url=/api/v1/portal/attachments/student-445/english_certificate/english_certificate-f4f9e3bf7fbd4446a151fdb510e7b87e.pdf` | `id=46` `application_id=70` `exam_name=CET-6` `score_text=599` `certificate_attachment_url=/api/v1/portal/attachments/student-445/english_certificate/english_certificate-a03039ffe72e4f489a984704156c0958.pdf` |
| 第 2 行 | `id=1989` `application_id=70` `exam_name=其他` `score_text=630` `certificate_attachment_url=/api/v1/portal/attachments/student-445/english_certificate/english_certificate-f4f9e3bf7fbd4446a151fdb510e7b87e.pdf` | `id=47` `application_id=70` `exam_name=其他` `score_text=630` `certificate_attachment_url=/api/v1/portal/attachments/student-445/english_certificate/english_certificate-f4f9e3bf7fbd4446a151fdb510e7b87e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270043

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1633` `application_id=73` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-539/english_certificate/english_certificate-ebef5113efc1407b92944e68a600dfbd.pdf` | `id=1081` `application_id=73` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-539/english_certificate/english_certificate-27f36f7c153b475d90c7aafb9174f717.pdf` |
| 第 2 行 | `id=1990` `application_id=73` `exam_name=CET-6` `score_text=573` `certificate_attachment_url=/api/v1/portal/attachments/student-539/english_certificate/english_certificate-ebef5113efc1407b92944e68a600dfbd.pdf` | `id=1082` `application_id=73` `exam_name=CET-6` `score_text=573` `certificate_attachment_url=/api/v1/portal/attachments/student-539/english_certificate/english_certificate-ebef5113efc1407b92944e68a600dfbd.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270048

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1747` `application_id=78` `exam_name=CET-6` `score_text=464` `certificate_attachment_url=/api/v1/portal/attachments/student-367/english_certificate/english_certificate-d3be2bb762fd4d4dbd5a4de05e88cea9.jpg` | `id=1132` `application_id=78` `exam_name=CET-6` `score_text=464` `certificate_attachment_url=/api/v1/portal/attachments/student-367/english_certificate/english_certificate-0bddde012d364421b1bcf7fd7caad0c0.jpg` |
| 第 2 行 | `id=1991` `application_id=78` `exam_name=IELTS` `score_text=5.5` `certificate_attachment_url=/api/v1/portal/attachments/student-367/english_certificate/english_certificate-d3be2bb762fd4d4dbd5a4de05e88cea9.jpg` | `id=1133` `application_id=78` `exam_name=IELTS` `score_text=5.5` `certificate_attachment_url=/api/v1/portal/attachments/student-367/english_certificate/english_certificate-d3be2bb762fd4d4dbd5a4de05e88cea9.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270053

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1727` `application_id=83` `exam_name=CET-6` `score_text=547` `certificate_attachment_url=/api/v1/portal/attachments/student-403/english_certificate/english_certificate-569487fc762f42629c4b7782e78216a1.pdf` | `id=62` `application_id=83` `exam_name=CET-6` `score_text=547` `certificate_attachment_url=/api/v1/portal/attachments/student-403/english_certificate/english_certificate-7247670e87764f79bd8f275a30f319c3.pdf` |
| 第 2 行 | `id=1992` `application_id=83` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-403/english_certificate/english_certificate-569487fc762f42629c4b7782e78216a1.pdf` | `id=63` `application_id=83` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-403/english_certificate/english_certificate-569487fc762f42629c4b7782e78216a1.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270054

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1734` `application_id=84` `exam_name=CET-6` `score_text=550` `certificate_attachment_url=/api/v1/portal/attachments/student-391/english_certificate/english_certificate-cebb3ede8a824514821da679448f362a.pdf` | `id=64` `application_id=84` `exam_name=CET-6` `score_text=550` `certificate_attachment_url=/api/v1/portal/attachments/student-391/english_certificate/english_certificate-5d2f1a129efc409e8d3fec89ce9fbb4f.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270057

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1755` `application_id=87` `exam_name=其他` `score_text=619` `certificate_attachment_url=/api/v1/portal/attachments/student-351/english_certificate/english_certificate-24f5ec1796aa48f3b3db06bf53bbd029.pdf` | `id=67` `application_id=87` `exam_name=其他` `score_text=619` `certificate_attachment_url=/api/v1/portal/attachments/student-351/english_certificate/english_certificate-135d6595d4f948e994db6bdae62c9181.jpg` |
| 第 2 行 | `id=1993` `application_id=87` `exam_name=CET-6` `score_text=622` `certificate_attachment_url=/api/v1/portal/attachments/student-351/english_certificate/english_certificate-24f5ec1796aa48f3b3db06bf53bbd029.pdf` | `id=68` `application_id=87` `exam_name=CET-6` `score_text=622` `certificate_attachment_url=/api/v1/portal/attachments/student-351/english_certificate/english_certificate-24f5ec1796aa48f3b3db06bf53bbd029.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270060

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1509` `application_id=90` `exam_name=CET-6` `score_text=435` `certificate_attachment_url=/api/v1/portal/attachments/student-734/english_certificate/english_certificate-bbd5a640eee3414b84a117556b589700.pdf` | `id=71` `application_id=90` `exam_name=CET-6` `score_text=435` `certificate_attachment_url=/api/v1/portal/attachments/student-734/english_certificate/english_certificate-c90e5153dd1a46f4b7090873be2f5c1a.pdf` |
| 第 2 行 | `id=1994` `application_id=90` `exam_name=其他` `score_text=530` `certificate_attachment_url=/api/v1/portal/attachments/student-734/english_certificate/english_certificate-bbd5a640eee3414b84a117556b589700.pdf` | `id=72` `application_id=90` `exam_name=其他` `score_text=530` `certificate_attachment_url=/api/v1/portal/attachments/student-734/english_certificate/english_certificate-bbd5a640eee3414b84a117556b589700.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270062

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1746` `application_id=92` `exam_name=CET-6` `score_text=512` `certificate_attachment_url=/api/v1/portal/attachments/student-371/english_certificate/english_certificate-e061af2274694b90a6ccfaf737c33d6e.pdf` | `id=74` `application_id=92` `exam_name=CET-6` `score_text=512` `certificate_attachment_url=/api/v1/portal/attachments/student-371/english_certificate/english_certificate-24665232f7fe43e898ff3c949ced15e6.pdf` |
| 第 2 行 | `id=1995` `application_id=92` `exam_name=其他` `score_text=549` `certificate_attachment_url=/api/v1/portal/attachments/student-371/english_certificate/english_certificate-e061af2274694b90a6ccfaf737c33d6e.pdf` | `id=75` `application_id=92` `exam_name=其他` `score_text=549` `certificate_attachment_url=/api/v1/portal/attachments/student-371/english_certificate/english_certificate-e061af2274694b90a6ccfaf737c33d6e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270072

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1897` `application_id=102` `exam_name=CET-6` `score_text=470` `certificate_attachment_url=/api/v1/portal/attachments/student-117/english_certificate/english_certificate-9948f92693cb4d8da3694a15b389a78e.pdf` | `id=790` `application_id=102` `exam_name=CET-6` `score_text=470` `certificate_attachment_url=/api/v1/portal/attachments/student-117/english_certificate/english_certificate-f4e62379c9b6479c97bb39ee03246db3.pdf` |
| 第 2 行 | `id=1996` `application_id=102` `exam_name=其他` `score_text=539` `certificate_attachment_url=/api/v1/portal/attachments/student-117/english_certificate/english_certificate-9948f92693cb4d8da3694a15b389a78e.pdf` | `id=791` `application_id=102` `exam_name=其他` `score_text=539` `certificate_attachment_url=/api/v1/portal/attachments/student-117/english_certificate/english_certificate-9948f92693cb4d8da3694a15b389a78e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270073

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1575` `application_id=103` `exam_name=CET-6` `score_text=529` `certificate_attachment_url=/api/v1/portal/attachments/student-627/english_certificate/english_certificate-881f61cc37dd4e2db451a1b34c1979ac.pdf` | `id=87` `application_id=103` `exam_name=CET-6` `score_text=529` `certificate_attachment_url=/api/v1/portal/attachments/student-627/english_certificate/english_certificate-69fb47e2d13640af915b7e3a4ef5482e.pdf` |
| 第 2 行 | `id=1997` `application_id=103` `exam_name=TOEFL` `score_text=92` `certificate_attachment_url=/api/v1/portal/attachments/student-627/english_certificate/english_certificate-881f61cc37dd4e2db451a1b34c1979ac.pdf` | `id=88` `application_id=103` `exam_name=TOEFL` `score_text=92` `certificate_attachment_url=/api/v1/portal/attachments/student-627/english_certificate/english_certificate-881f61cc37dd4e2db451a1b34c1979ac.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270076

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1544` `application_id=107` `exam_name=其他` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-676/english_certificate/english_certificate-7ee1d3e9484d4fc991b4405b0fb4e626.pdf` | `id=93` `application_id=107` `exam_name=其他` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-676/english_certificate/english_certificate-9df816af45234252856f3807a12da02f.pdf` |
| 第 2 行 | `id=1998` `application_id=107` `exam_name=CET-6` `score_text=499` `certificate_attachment_url=/api/v1/portal/attachments/student-676/english_certificate/english_certificate-7ee1d3e9484d4fc991b4405b0fb4e626.pdf` | `id=94` `application_id=107` `exam_name=CET-6` `score_text=499` `certificate_attachment_url=/api/v1/portal/attachments/student-676/english_certificate/english_certificate-7ee1d3e9484d4fc991b4405b0fb4e626.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270078

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1635` `application_id=111` `exam_name=CET-6` `score_text=578` `certificate_attachment_url=/api/v1/portal/attachments/student-537/english_certificate/english_certificate-5172b03bf16c4344a7004d75079f317a.pdf` | `id=98` `application_id=111` `exam_name=CET-6` `score_text=578` `certificate_attachment_url=/api/v1/portal/attachments/student-537/english_certificate/english_certificate-abc264bcb9e04262a31d2cc03f544b1a.pdf` |
| 第 2 行 | `id=1999` `application_id=111` `exam_name=其他` `score_text=CET4 587` `certificate_attachment_url=/api/v1/portal/attachments/student-537/english_certificate/english_certificate-5172b03bf16c4344a7004d75079f317a.pdf` | `id=99` `application_id=111` `exam_name=其他` `score_text=CET4 587` `certificate_attachment_url=/api/v1/portal/attachments/student-537/english_certificate/english_certificate-5172b03bf16c4344a7004d75079f317a.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270079

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1628` `application_id=112` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-547/english_certificate/english_certificate-3f4eb3c3d490416f863e61b1d9ab4230.pdf` | `id=100` `application_id=112` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-547/english_certificate/english_certificate-4da62052bdeb47fc9c38908cf1f6aad7.pdf` |
| 第 2 行 | `id=2000` `application_id=112` `exam_name=CET-6` `score_text=546` `certificate_attachment_url=/api/v1/portal/attachments/student-547/english_certificate/english_certificate-3f4eb3c3d490416f863e61b1d9ab4230.pdf` | `id=101` `application_id=112` `exam_name=CET-6` `score_text=546` `certificate_attachment_url=/api/v1/portal/attachments/student-547/english_certificate/english_certificate-3f4eb3c3d490416f863e61b1d9ab4230.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270084

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1516` `application_id=118` `exam_name=CET-6` `score_text=455` `certificate_attachment_url=/api/v1/portal/attachments/student-722/english_certificate/english_certificate-24d2425fbb57419393ddfeee3aeb4409.pdf` | `id=1061` `application_id=118` `exam_name=CET-6` `score_text=455` `certificate_attachment_url=/api/v1/portal/attachments/student-722/english_certificate/english_certificate-e210d340ceee4257afcc1b021851e603.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270086

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1507` `application_id=120` `exam_name=TOEFL` `score_text=100` `certificate_attachment_url=/api/v1/portal/attachments/student-737/english_certificate/english_certificate-d303e36028114db687cb5dd8600485e7.pdf` | `id=109` `application_id=120` `exam_name=TOEFL` `score_text=100` `certificate_attachment_url=/api/v1/portal/attachments/student-737/english_certificate/english_certificate-d410b16ce6314f98a006d09bb7d9e7db.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270090

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1960` `application_id=125` `exam_name=CET-6` `score_text=495` `certificate_attachment_url=/api/v1/portal/attachments/student-35/english_certificate/english_certificate-b81cb31869dd4a1c9c71fb37aa29f129.pdf` | `id=114` `application_id=125` `exam_name=CET-6` `score_text=495` `certificate_attachment_url=/api/v1/portal/attachments/student-35/english_certificate/english_certificate-d193dec4189e4795b094552a55901b26.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270096

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1766` `application_id=132` `exam_name=CET-6` `score_text=535` `certificate_attachment_url=/api/v1/portal/attachments/student-331/english_certificate/english_certificate-c7b24461be594933bf59814201360a30.pdf` | `id=121` `application_id=132` `exam_name=CET-6` `score_text=535` `certificate_attachment_url=/api/v1/portal/attachments/student-331/english_certificate/english_certificate-c8dbce9d823d4bc680984d3e8a01f50d.pdf` |
| 第 2 行 | `id=2001` `application_id=132` `exam_name=其他` `score_text=558` `certificate_attachment_url=/api/v1/portal/attachments/student-331/english_certificate/english_certificate-c7b24461be594933bf59814201360a30.pdf` | `id=122` `application_id=132` `exam_name=其他` `score_text=558` `certificate_attachment_url=/api/v1/portal/attachments/student-331/english_certificate/english_certificate-c7b24461be594933bf59814201360a30.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270101

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1724` `application_id=137` `exam_name=CET-6` `score_text=638` `certificate_attachment_url=/api/v1/portal/attachments/student-407/english_certificate/english_certificate-64e290cea1304229ad8be4ccfaae07b5.pdf` | `id=127` `application_id=137` `exam_name=CET-6` `score_text=638` `certificate_attachment_url=/api/v1/portal/attachments/student-407/english_certificate/english_certificate-2a7167a1c48e4532bb8e67b91965ebb4.pdf` |
| 第 2 行 | `id=2002` `application_id=137` `exam_name=TOEFL` `score_text=112` `certificate_attachment_url=/api/v1/portal/attachments/student-407/english_certificate/english_certificate-64e290cea1304229ad8be4ccfaae07b5.pdf` | `id=128` `application_id=137` `exam_name=TOEFL` `score_text=112` `certificate_attachment_url=/api/v1/portal/attachments/student-407/english_certificate/english_certificate-64e290cea1304229ad8be4ccfaae07b5.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270104

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1949` `application_id=140` `exam_name=CET-6` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-49/english_certificate/english_certificate-ee6bc80ac5b845029b8ff5df03afaa5d.pdf` | `id=1185` `application_id=140` `exam_name=CET-6` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-49/english_certificate/english_certificate-7b36567f64f846f398d6e1bc9a48756e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270106

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1823` `application_id=142` `exam_name=CET-6` `score_text=576` `certificate_attachment_url=/api/v1/portal/attachments/student-226/english_certificate/english_certificate-a513889e62d94b598df8ee259b5e13f2.pdf` | `id=133` `application_id=142` `exam_name=CET-6` `score_text=576` `certificate_attachment_url=/api/v1/portal/attachments/student-226/english_certificate/english_certificate-ff554b6e4bc8401b84358b9d6af37342.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270110

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1877` `application_id=146` `exam_name=CET-6` `score_text=564` `certificate_attachment_url=/api/v1/portal/attachments/student-147/english_certificate/english_certificate-57054c6b9ed6475ab07f48a54432d2a6.pdf` | `id=137` `application_id=146` `exam_name=CET-6` `score_text=564` `certificate_attachment_url=/api/v1/portal/attachments/student-147/english_certificate/english_certificate-4649900e054b40a8a414154b3d72eb53.pdf` |
| 第 2 行 | `id=1878` `application_id=146` `exam_name=TOEFL` `score_text=96` `certificate_attachment_url=/api/v1/portal/attachments/student-147/english_certificate/english_certificate-b0c04fa025aa49c4b1955f32261d4a5b.pdf` | `id=138` `application_id=146` `exam_name=TOEFL` `score_text=96` `certificate_attachment_url=/api/v1/portal/attachments/student-147/english_certificate/english_certificate-60f19e37640649edb2ea1828dfb5a59d.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270111

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1872` `application_id=147` `exam_name=CET-6` `score_text=455` `certificate_attachment_url=/api/v1/portal/attachments/student-156/english_certificate/english_certificate-b95490402842413d94d5b366c3904288.jpg` | `id=139` `application_id=147` `exam_name=CET-6` `score_text=455` `certificate_attachment_url=/api/v1/portal/attachments/student-156/english_certificate/english_certificate-ab8ca988f23f4bc79a9a5a80c34bdd23.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270113

- 主库行数：4
- 备库行数：4
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1630` `application_id=149` `exam_name=CET-6` `score_text=559` `certificate_attachment_url=/api/v1/portal/attachments/student-544/english_certificate/english_certificate-a22aca69d44c471bb56adbfb8f0b907f.pdf` | `id=1165` `application_id=149` `exam_name=CET-6` `score_text=559` `certificate_attachment_url=/api/v1/portal/attachments/student-544/english_certificate/english_certificate-4e2b725e1ed843748b57d5823a7b9b56.pdf` |
| 第 2 行 | `id=2003` `application_id=149` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-544/english_certificate/english_certificate-1943b774bf094da5899d5c9e5d5a1ae6.pdf` | `id=1166` `application_id=149` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-544/english_certificate/english_certificate-1943b774bf094da5899d5c9e5d5a1ae6.pdf` |
| 第 3 行 | `id=2004` `application_id=149` `exam_name=其他` `score_text=322` `certificate_attachment_url=/api/v1/portal/attachments/student-544/english_certificate/english_certificate-dcd4352feed64e008d0ea272c7fdf02a.pdf` | `id=1167` `application_id=149` `exam_name=其他` `score_text=322` `certificate_attachment_url=/api/v1/portal/attachments/student-544/english_certificate/english_certificate-dcd4352feed64e008d0ea272c7fdf02a.pdf` |
| 第 4 行 | `id=2005` `application_id=149` `exam_name=其他` `score_text=641` `certificate_attachment_url=/api/v1/portal/attachments/student-544/english_certificate/english_certificate-a22aca69d44c471bb56adbfb8f0b907f.pdf` | `id=1168` `application_id=149` `exam_name=其他` `score_text=641` `certificate_attachment_url=/api/v1/portal/attachments/student-544/english_certificate/english_certificate-a22aca69d44c471bb56adbfb8f0b907f.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270117

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1477` `application_id=153` `exam_name=CET-6` `score_text=502` `certificate_attachment_url=/api/v1/portal/attachments/student-778/english_certificate/english_certificate-edeabcf7dd034f20b22dbd989e85d3a8.jpg` | `id=149` `application_id=153` `exam_name=CET-6` `score_text=502` `certificate_attachment_url=/api/v1/portal/attachments/student-778/english_certificate/english_certificate-54b45e3616a24d388bf5aef367a95290.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270122

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1830` `application_id=158` `exam_name=CET-6` `score_text=567` `certificate_attachment_url=/api/v1/portal/attachments/student-215/english_certificate/english_certificate-0afa853af80d487cae182d50997132b8.pdf` | `id=960` `application_id=158` `exam_name=CET-6` `score_text=567` `certificate_attachment_url=/api/v1/portal/attachments/student-215/english_certificate/english_certificate-5a0933ef0c564701bbd7d8a35a83d0ed.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270126

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1683` `application_id=162` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-469/english_certificate/english_certificate-ee575c4d931e4ac381740b95ac93537a.pdf` | `id=158` `application_id=162` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-469/english_certificate/english_certificate-f8ab010720bc4bd3b14516be1657ad6a.pdf` |
| 第 2 行 | `id=2006` `application_id=162` `exam_name=其他` `score_text=578` `certificate_attachment_url=/api/v1/portal/attachments/student-469/english_certificate/english_certificate-ee575c4d931e4ac381740b95ac93537a.pdf` | `id=159` `application_id=162` `exam_name=其他` `score_text=578` `certificate_attachment_url=/api/v1/portal/attachments/student-469/english_certificate/english_certificate-ee575c4d931e4ac381740b95ac93537a.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270129

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1759` `application_id=165` `exam_name=CET-6` `score_text=426` `certificate_attachment_url=/api/v1/portal/attachments/student-344/english_certificate/english_certificate-1735e78944d54776a9d82d57cb0ea641.pdf` | `id=164` `application_id=165` `exam_name=CET-6` `score_text=426` `certificate_attachment_url=/api/v1/portal/attachments/student-344/english_certificate/english_certificate-0a80affa861d4938bf44497e23eb9352.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270144

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1732` `application_id=180` `exam_name=CET-6` `score_text=566` `certificate_attachment_url=/api/v1/portal/attachments/student-393/english_certificate/english_certificate-b92da46fc95240a99048e658679a969f.pdf` | `id=179` `application_id=180` `exam_name=CET-6` `score_text=566` `certificate_attachment_url=/api/v1/portal/attachments/student-393/english_certificate/english_certificate-3d9312c09c7146adbdae91f36f474088.pdf` |
| 第 2 行 | `id=2007` `application_id=180` `exam_name=其他` `score_text=594` `certificate_attachment_url=/api/v1/portal/attachments/student-393/english_certificate/english_certificate-b92da46fc95240a99048e658679a969f.pdf` | `id=180` `application_id=180` `exam_name=其他` `score_text=594` `certificate_attachment_url=/api/v1/portal/attachments/student-393/english_certificate/english_certificate-b92da46fc95240a99048e658679a969f.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270149

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1629` `application_id=185` `exam_name=IELTS` `score_text=6.0` `certificate_attachment_url=/api/v1/portal/attachments/student-545/english_certificate/english_certificate-df7f285260874b7780bf38176cb80d87.pdf` | `id=1159` `application_id=185` `exam_name=IELTS` `score_text=6.0` `certificate_attachment_url=/api/v1/portal/attachments/student-545/english_certificate/english_certificate-ae4d79008a934c299978d56fd353e79a.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270151

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1744` `application_id=187` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-375/english_certificate/english_certificate-d2407915fe4d4ddf856d8284f3b902b4.pdf` | `id=187` `application_id=187` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-375/english_certificate/english_certificate-5400ab92d73e4baf9e5450dbd3876ecf.pdf` |
| 第 2 行 | `id=2008` `application_id=187` `exam_name=CET-6` `score_text=525` `certificate_attachment_url=/api/v1/portal/attachments/student-375/english_certificate/english_certificate-d2407915fe4d4ddf856d8284f3b902b4.pdf` | `id=188` `application_id=187` `exam_name=CET-6` `score_text=525` `certificate_attachment_url=/api/v1/portal/attachments/student-375/english_certificate/english_certificate-d2407915fe4d4ddf856d8284f3b902b4.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270152

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1428` `application_id=188` `exam_name=CET-6` `score_text=602` `certificate_attachment_url=/api/v1/portal/attachments/student-851/english_certificate/english_certificate-28a4c17acc6e4aa5bdb6bce93889a57c.pdf` | `id=189` `application_id=188` `exam_name=CET-6` `score_text=602` `certificate_attachment_url=/api/v1/portal/attachments/student-851/english_certificate/english_certificate-0dcc32447e2544a5b854a1885511b711.pdf` |
| 第 2 行 | `id=2009` `application_id=188` `exam_name=其他` `score_text=642` `certificate_attachment_url=/api/v1/portal/attachments/student-851/english_certificate/english_certificate-e4175c182f1649ea9a14c6c3e239d042.pdf` | `id=190` `application_id=188` `exam_name=其他` `score_text=642` `certificate_attachment_url=/api/v1/portal/attachments/student-851/english_certificate/english_certificate-e4175c182f1649ea9a14c6c3e239d042.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270154

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1546` `application_id=190` `exam_name=CET-6` `score_text=547` `certificate_attachment_url=/api/v1/portal/attachments/student-672/english_certificate/english_certificate-abe58f31f7c7415ca563e83bd3fbff0f.pdf` | `id=192` `application_id=190` `exam_name=CET-6` `score_text=547` `certificate_attachment_url=/api/v1/portal/attachments/student-672/english_certificate/english_certificate-03b4060d9fb84107b4ffacd933a8bcb6.pdf` |
| 第 2 行 | `id=2010` `application_id=190` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-672/english_certificate/english_certificate-abe58f31f7c7415ca563e83bd3fbff0f.pdf` | `id=193` `application_id=190` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-672/english_certificate/english_certificate-abe58f31f7c7415ca563e83bd3fbff0f.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270160

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1380` `application_id=196` `exam_name=其他` `score_text=560` `certificate_attachment_url=/api/v1/portal/attachments/student-908/english_certificate/english_certificate-848f1cb4674c4ae5a943fe3897fff361.pdf` | `id=199` `application_id=196` `exam_name=其他` `score_text=560` `certificate_attachment_url=/api/v1/portal/attachments/student-908/english_certificate/english_certificate-f4c034cfd1de4b63b78af268f4fab747.pdf` |
| 第 2 行 | `id=2011` `application_id=196` `exam_name=CET-6` `score_text=476` `certificate_attachment_url=/api/v1/portal/attachments/student-908/english_certificate/english_certificate-68cce5ae22134a109db401f5b62ea147.pdf` | `id=200` `application_id=196` `exam_name=CET-6` `score_text=476` `certificate_attachment_url=/api/v1/portal/attachments/student-908/english_certificate/english_certificate-68cce5ae22134a109db401f5b62ea147.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270162

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1407` `application_id=198` `exam_name=CET-6` `score_text=519` `certificate_attachment_url=/api/v1/portal/attachments/student-873/english_certificate/english_certificate-02f04563c7df41b48caf669b4d4fa4b8.pdf` | `id=1072` `application_id=198` `exam_name=CET-6` `score_text=519` `certificate_attachment_url=/api/v1/portal/attachments/student-873/english_certificate/english_certificate-84a720cdb5664af89403b603aaf3cae6.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270167

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1857` `application_id=203` `exam_name=CET-6` `score_text=583` `certificate_attachment_url=/api/v1/portal/attachments/student-174/english_certificate/english_certificate-3fbd2f2f5d994aab86d97f119964e929.pdf` | `id=208` `application_id=203` `exam_name=CET-6` `score_text=583` `certificate_attachment_url=/api/v1/portal/attachments/student-174/english_certificate/english_certificate-6b3df4e6168e4284aa2da04580f4e190.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270171

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1909` `application_id=207` `exam_name=CET-6` `score_text=534` `certificate_attachment_url=/api/v1/portal/attachments/student-102/english_certificate/english_certificate-7884c6c1c52b463f8f4d4b5e4fc355a7.pdf` | `id=212` `application_id=207` `exam_name=CET-6` `score_text=534` `certificate_attachment_url=/api/v1/portal/attachments/student-102/english_certificate/english_certificate-f40c4ea3375f4a04bf72fc283eb6d0f5.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270173

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1904` `application_id=208` `exam_name=CET-6` `score_text=499` `certificate_attachment_url=/api/v1/portal/attachments/student-109/english_certificate/english_certificate-f15485facad84bf69a560d1b9aa24d54.pdf` | `id=214` `application_id=208` `exam_name=CET-6` `score_text=499` `certificate_attachment_url=/api/v1/portal/attachments/student-109/english_certificate/english_certificate-6cae44d26a144a05bc52d2b0480dd548.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270175

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1787` `application_id=210` `exam_name=CET-6` `score_text=539` `certificate_attachment_url=/api/v1/portal/attachments/student-291/english_certificate/english_certificate-386defcc3a944fb59b8c1185c486f97b.pdf` | `id=216` `application_id=210` `exam_name=CET-6` `score_text=539` `certificate_attachment_url=/api/v1/portal/attachments/student-291/english_certificate/english_certificate-e8b2bb481f304ff4bb9f382c56ed503d.pdf` |
| 第 2 行 | `id=2012` `application_id=210` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-291/english_certificate/english_certificate-386defcc3a944fb59b8c1185c486f97b.pdf` | `id=217` `application_id=210` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-291/english_certificate/english_certificate-386defcc3a944fb59b8c1185c486f97b.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270183

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1647` `application_id=218` `exam_name=TOEFL` `score_text=90` `certificate_attachment_url=/api/v1/portal/attachments/student-519/english_certificate/english_certificate-2a4d8e8dba774db889a9c128b3662846.pdf` | `id=225` `application_id=218` `exam_name=TOEFL` `score_text=90` `certificate_attachment_url=/api/v1/portal/attachments/student-519/english_certificate/english_certificate-ca6a73064d624c3cae322d5631f1f6ba.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270184

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1885` `application_id=219` `exam_name=IELTS` `score_text=5.5` `certificate_attachment_url=/api/v1/portal/attachments/student-138/english_certificate/english_certificate-e21e016c927b42b79cda999da421f9e1.pdf` | `id=226` `application_id=219` `exam_name=IELTS` `score_text=5.5` `certificate_attachment_url=/api/v1/portal/attachments/student-138/english_certificate/english_certificate-e396f85103004ef9af3fde3a964621b0.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270190

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1298` `application_id=225` `exam_name=其他` `score_text=434` `certificate_attachment_url=/api/v1/portal/attachments/student-1027/english_certificate/english_certificate-5f204d86fa0b42aeb0e580ec212dcd02.png` | `id=232` `application_id=225` `exam_name=其他` `score_text=434` `certificate_attachment_url=/api/v1/portal/attachments/student-1027/english_certificate/english_certificate-7f218122e23e4f368acbf8e766e4b648.png` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270197

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1642` `application_id=232` `exam_name=CET-6` `score_text=477` `certificate_attachment_url=/api/v1/portal/attachments/student-528/english_certificate/english_certificate-fb10ce95c46c4ea9863ef8cb6998ea58.pdf` | `id=239` `application_id=232` `exam_name=CET-6` `score_text=477` `certificate_attachment_url=/api/v1/portal/attachments/student-528/english_certificate/english_certificate-436a018f1d6e4127bef631a65324cefc.pdf` |
| 第 2 行 | `id=2013` `application_id=232` `exam_name=其他` `score_text=317` `certificate_attachment_url=/api/v1/portal/attachments/student-528/english_certificate/english_certificate-fb10ce95c46c4ea9863ef8cb6998ea58.pdf` | `id=240` `application_id=232` `exam_name=其他` `score_text=317` `certificate_attachment_url=/api/v1/portal/attachments/student-528/english_certificate/english_certificate-fb10ce95c46c4ea9863ef8cb6998ea58.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270198

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1447` `application_id=233` `exam_name=CET-6` `score_text=579` `certificate_attachment_url=/api/v1/portal/attachments/student-827/english_certificate/english_certificate-e63ee66dab5949b582f2549004c39106.pdf` | `id=241` `application_id=233` `exam_name=CET-6` `score_text=579` `certificate_attachment_url=/api/v1/portal/attachments/student-827/english_certificate/english_certificate-02cef5600889496e8e00ab1efc45a314.pdf` |
| 第 2 行 | `id=2014` `application_id=233` `exam_name=其他` `score_text=618` `certificate_attachment_url=/api/v1/portal/attachments/student-827/english_certificate/english_certificate-e63ee66dab5949b582f2549004c39106.pdf` | `id=242` `application_id=233` `exam_name=其他` `score_text=618` `certificate_attachment_url=/api/v1/portal/attachments/student-827/english_certificate/english_certificate-e63ee66dab5949b582f2549004c39106.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270199

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1347` `application_id=234` `exam_name=CET-6` `score_text=513` `certificate_attachment_url=/api/v1/portal/attachments/student-960/english_certificate/english_certificate-28d2d05612124e69bda182886bbb35f4.pdf` | `id=243` `application_id=234` `exam_name=CET-6` `score_text=513` `certificate_attachment_url=/api/v1/portal/attachments/student-960/english_certificate/english_certificate-d176806501b04441b61bd1f011e8ec3d.pdf` |
| 第 2 行 | `id=2015` `application_id=234` `exam_name=其他` `score_text=大学生英语竞赛国家三等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-960/english_certificate/english_certificate-53552a0447a141198455933c475f64a5.jpg` | `id=244` `application_id=234` `exam_name=其他` `score_text=大学生英语竞赛国家三等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-960/english_certificate/english_certificate-53552a0447a141198455933c475f64a5.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270205

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1936` `application_id=240` `exam_name=CET-6` `score_text=545` `certificate_attachment_url=/api/v1/portal/attachments/student-66/english_certificate/english_certificate-553e9a5391694844a0d8c8a882dae7f5.pdf` | `id=775` `application_id=240` `exam_name=CET-6` `score_text=545` `certificate_attachment_url=/api/v1/portal/attachments/student-66/english_certificate/english_certificate-f2a4e284bada414099fa1e9d804f7d82.pdf` |
| 第 2 行 | `id=2016` `application_id=240` `exam_name=其他` `score_text=CET-4 571` `certificate_attachment_url=/api/v1/portal/attachments/student-66/english_certificate/english_certificate-553e9a5391694844a0d8c8a882dae7f5.pdf` | `id=776` `application_id=240` `exam_name=其他` `score_text=CET-4 571` `certificate_attachment_url=/api/v1/portal/attachments/student-66/english_certificate/english_certificate-553e9a5391694844a0d8c8a882dae7f5.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270217

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1493` `application_id=252` `exam_name=CET-6` `score_text=445` `certificate_attachment_url=/api/v1/portal/attachments/student-755/english_certificate/english_certificate-888b2ceab28342a6a78c14a5be74f584.pdf` | `id=263` `application_id=252` `exam_name=CET-6` `score_text=445` `certificate_attachment_url=/api/v1/portal/attachments/student-755/english_certificate/english_certificate-102db2ea530f4521a0eac9f566607d93.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270219

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1606` `application_id=254` `exam_name=CET-6` `score_text=482` `certificate_attachment_url=/api/v1/portal/attachments/student-581/english_certificate/english_certificate-1caebc071c7c4eafaa16d98f2ebee86e.pdf` | `id=265` `application_id=254` `exam_name=CET-6` `score_text=482` `certificate_attachment_url=/api/v1/portal/attachments/student-581/english_certificate/english_certificate-8bbd805493374e68999755d631763e77.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270223

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1969` `application_id=259` `exam_name=CET-6` `score_text=558` `certificate_attachment_url=/api/v1/portal/attachments/student-24/english_certificate/english_certificate-0a8be1adeb134ee8b62d606b3b7c48a1.pdf` | `id=271` `application_id=259` `exam_name=CET-6` `score_text=558` `certificate_attachment_url=/api/v1/portal/attachments/student-24/english_certificate/english_certificate-18ae78ea5a844091b03d238d63f5c70e.pdf` |
| 第 2 行 | `id=2017` `application_id=259` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-24/english_certificate/english_certificate-0a8be1adeb134ee8b62d606b3b7c48a1.pdf` | `id=272` `application_id=259` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-24/english_certificate/english_certificate-0a8be1adeb134ee8b62d606b3b7c48a1.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270224

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1278` `application_id=260` `exam_name=CET-6` `score_text=600` `certificate_attachment_url=/api/v1/portal/attachments/student-1049/english_certificate/english_certificate-753c2c7a23cb47c2a16680ea2616b05e.pdf` | `id=273` `application_id=260` `exam_name=CET-6` `score_text=600` `certificate_attachment_url=/api/v1/portal/attachments/student-1049/english_certificate/english_certificate-a89ff6811db14404a6b2204e8d95892d.pdf` |
| 第 2 行 | `id=2018` `application_id=260` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1049/english_certificate/english_certificate-753c2c7a23cb47c2a16680ea2616b05e.pdf` | `id=274` `application_id=260` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1049/english_certificate/english_certificate-753c2c7a23cb47c2a16680ea2616b05e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270226

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1600` `application_id=262` `exam_name=CET-6` `score_text=581` `certificate_attachment_url=/api/v1/portal/attachments/student-590/english_certificate/english_certificate-8f36d45439934255abcc208291978994.pdf` | `id=276` `application_id=262` `exam_name=CET-6` `score_text=581` `certificate_attachment_url=/api/v1/portal/attachments/student-590/english_certificate/english_certificate-7d07f50a0e864b369573788c2f246aa3.pdf` |
| 第 2 行 | `id=2019` `application_id=262` `exam_name=TOEFL` `score_text=92` `certificate_attachment_url=/api/v1/portal/attachments/student-590/english_certificate/english_certificate-8f36d45439934255abcc208291978994.pdf` | `id=277` `application_id=262` `exam_name=TOEFL` `score_text=92` `certificate_attachment_url=/api/v1/portal/attachments/student-590/english_certificate/english_certificate-8f36d45439934255abcc208291978994.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270227

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1524` `application_id=263` `exam_name=CET-6` `score_text=603` `certificate_attachment_url=/api/v1/portal/attachments/student-706/english_certificate/english_certificate-1cfd6586f34c4746943ffba79fa1a023.pdf` | `id=278` `application_id=263` `exam_name=CET-6` `score_text=603` `certificate_attachment_url=/api/v1/portal/attachments/student-706/english_certificate/english_certificate-51a16f5fd368433db9a898f984ba19ca.pdf` |
| 第 2 行 | `id=2020` `application_id=263` `exam_name=其他` `score_text=630` `certificate_attachment_url=/api/v1/portal/attachments/student-706/english_certificate/english_certificate-4ccf7c8f6b754274ae067888514b2c6d.pdf` | `id=279` `application_id=263` `exam_name=其他` `score_text=630` `certificate_attachment_url=/api/v1/portal/attachments/student-706/english_certificate/english_certificate-4ccf7c8f6b754274ae067888514b2c6d.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270233

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1277` `application_id=269` `exam_name=CET-6` `score_text=550` `certificate_attachment_url=/api/v1/portal/attachments/student-1051/english_certificate/english_certificate-542cc5d53b0e41fbb8606373491b5f14.pdf` | `id=285` `application_id=269` `exam_name=CET-6` `score_text=550` `certificate_attachment_url=/api/v1/portal/attachments/student-1051/english_certificate/english_certificate-85e2127dd141454096941359d8ce5a46.pdf` |
| 第 2 行 | `id=2021` `application_id=269` `exam_name=其他` `score_text=611` `certificate_attachment_url=/api/v1/portal/attachments/student-1051/english_certificate/english_certificate-542cc5d53b0e41fbb8606373491b5f14.pdf` | `id=286` `application_id=269` `exam_name=其他` `score_text=611` `certificate_attachment_url=/api/v1/portal/attachments/student-1051/english_certificate/english_certificate-542cc5d53b0e41fbb8606373491b5f14.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270235

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1776` `application_id=271` `exam_name=CET-6` `score_text=556` `certificate_attachment_url=/api/v1/portal/attachments/student-317/english_certificate/english_certificate-1bb3283a6df34e84be1aed9277357fc5.pdf` | `id=820` `application_id=271` `exam_name=CET-6` `score_text=556` `certificate_attachment_url=/api/v1/portal/attachments/student-317/english_certificate/english_certificate-5431f92c86824591890f8724e10a1ade.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270237

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1810` `application_id=273` `exam_name=CET-6` `score_text=543` `certificate_attachment_url=/api/v1/portal/attachments/student-251/english_certificate/english_certificate-e3d8f61408e34caa8f7156b05a467013.pdf` | `id=290` `application_id=273` `exam_name=CET-6` `score_text=543` `certificate_attachment_url=/api/v1/portal/attachments/student-251/english_certificate/english_certificate-e7ebdc93c18d458586105be020a00752.pdf` |
| 第 2 行 | `id=2022` `application_id=273` `exam_name=其他` `score_text=638` `certificate_attachment_url=/api/v1/portal/attachments/student-251/english_certificate/english_certificate-d90a15186db6435c9ba67a9738a5009d.pdf` | `id=291` `application_id=273` `exam_name=其他` `score_text=638` `certificate_attachment_url=/api/v1/portal/attachments/student-251/english_certificate/english_certificate-d90a15186db6435c9ba67a9738a5009d.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270241

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1937` `application_id=277` `exam_name=TOEFL` `score_text=108` `certificate_attachment_url=/api/v1/portal/attachments/student-65/english_certificate/english_certificate-c6a8fd83a5064fdb838cac1b33b501f6.pdf` | `id=295` `application_id=277` `exam_name=TOEFL` `score_text=108` `certificate_attachment_url=/api/v1/portal/attachments/student-65/english_certificate/english_certificate-3aa6da472f134725a36e7fee6c31ca3e.pdf` |
| 第 2 行 | `id=2023` `application_id=277` `exam_name=CET-6` `score_text=634` `certificate_attachment_url=/api/v1/portal/attachments/student-65/english_certificate/english_certificate-c6a8fd83a5064fdb838cac1b33b501f6.pdf` | `id=296` `application_id=277` `exam_name=CET-6` `score_text=634` `certificate_attachment_url=/api/v1/portal/attachments/student-65/english_certificate/english_certificate-c6a8fd83a5064fdb838cac1b33b501f6.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270242

- 主库行数：3
- 备库行数：3
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1443` `application_id=278` `exam_name=CET-6` `score_text=556` `certificate_attachment_url=/api/v1/portal/attachments/student-833/english_certificate/english_certificate-cfc02b446cc6423a90efbcc9383067c0.pdf` | `id=297` `application_id=278` `exam_name=CET-6` `score_text=556` `certificate_attachment_url=/api/v1/portal/attachments/student-833/english_certificate/english_certificate-d70b1f01d0644221bc9a32b3e127cb06.pdf` |
| 第 2 行 | `id=2024` `application_id=278` `exam_name=TOEFL` `score_text=86` `certificate_attachment_url=/api/v1/portal/attachments/student-833/english_certificate/english_certificate-508cfd39f5324c619e9c75e4bcb995de.jpg` | `id=298` `application_id=278` `exam_name=TOEFL` `score_text=86` `certificate_attachment_url=/api/v1/portal/attachments/student-833/english_certificate/english_certificate-508cfd39f5324c619e9c75e4bcb995de.jpg` |
| 第 3 行 | `id=2025` `application_id=278` `exam_name=其他` `score_text=600` `certificate_attachment_url=/api/v1/portal/attachments/student-833/english_certificate/english_certificate-cfc02b446cc6423a90efbcc9383067c0.pdf` | `id=299` `application_id=278` `exam_name=其他` `score_text=600` `certificate_attachment_url=/api/v1/portal/attachments/student-833/english_certificate/english_certificate-cfc02b446cc6423a90efbcc9383067c0.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270252

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1553` `application_id=289` `exam_name=CET-6` `score_text=604` `certificate_attachment_url=/api/v1/portal/attachments/student-664/english_certificate/english_certificate-c2361e4c55f84bf893abe0017e328cd7.pdf` | `id=311` `application_id=289` `exam_name=CET-6` `score_text=604` `certificate_attachment_url=/api/v1/portal/attachments/student-664/english_certificate/english_certificate-5aa68dfedfd2474098892782cb343702.pdf` |
| 第 2 行 | `id=2026` `application_id=289` `exam_name=TOEFL` `score_text=96` `certificate_attachment_url=/api/v1/portal/attachments/student-664/english_certificate/english_certificate-c2361e4c55f84bf893abe0017e328cd7.pdf` | `id=312` `application_id=289` `exam_name=TOEFL` `score_text=96` `certificate_attachment_url=/api/v1/portal/attachments/student-664/english_certificate/english_certificate-c2361e4c55f84bf893abe0017e328cd7.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270255

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1954` `application_id=105` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-43/english_certificate/english_certificate-d1aade67e01d4bd6a1a10c35e52737c5.pdf` | `id=315` `application_id=105` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-43/english_certificate/english_certificate-012e41173b3d4e31ad9ef5d98268e355.pdf` |
| 第 2 行 | `id=2027` `application_id=105` `exam_name=其他` `score_text=全国大学生英语竞赛特等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-43/english_certificate/english_certificate-d1aade67e01d4bd6a1a10c35e52737c5.pdf` | `id=316` `application_id=105` `exam_name=其他` `score_text=全国大学生英语竞赛特等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-43/english_certificate/english_certificate-d1aade67e01d4bd6a1a10c35e52737c5.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270264

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1484` `application_id=300` `exam_name=CET-6` `score_text=597` `certificate_attachment_url=/api/v1/portal/attachments/student-769/english_certificate/english_certificate-bf3ee9920e764fb58dc4e777bac1b41c.pdf` | `id=325` `application_id=300` `exam_name=CET-6` `score_text=597` `certificate_attachment_url=/api/v1/portal/attachments/student-769/english_certificate/english_certificate-4c48b51d79ac48c6ad3bb638bed5842f.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270270

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1159` `application_id=306` `exam_name=CET-6` `score_text=522` `certificate_attachment_url=/api/v1/portal/attachments/student-1222/english_certificate/english_certificate-cc59a309f8494b5583b0590ecf444a39.pdf` | `id=331` `application_id=306` `exam_name=CET-6` `score_text=522` `certificate_attachment_url=/api/v1/portal/attachments/student-1222/english_certificate/english_certificate-a1cc3df134264cc6829391e1388d9768.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270272

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1670` `application_id=308` `exam_name=CET-6` `score_text=645` `certificate_attachment_url=/api/v1/portal/attachments/student-488/english_certificate/english_certificate-4230cb9a7f804728b1042c823f3950a3.pdf` | `id=808` `application_id=308` `exam_name=CET-6` `score_text=645` `certificate_attachment_url=/api/v1/portal/attachments/student-488/english_certificate/english_certificate-381b2492749b42659f4cb9aee4a65229.pdf` |
| 第 2 行 | `id=2028` `application_id=308` `exam_name=其他` `score_text=CET-4 685` `certificate_attachment_url=/api/v1/portal/attachments/student-488/english_certificate/english_certificate-4230cb9a7f804728b1042c823f3950a3.pdf` | `id=809` `application_id=308` `exam_name=其他` `score_text=CET-4 685` `certificate_attachment_url=/api/v1/portal/attachments/student-488/english_certificate/english_certificate-4230cb9a7f804728b1042c823f3950a3.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270279

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1896` `application_id=315` `exam_name=CET-6` `score_text=576` `certificate_attachment_url=/api/v1/portal/attachments/student-120/english_certificate/english_certificate-e867457d5c154a0498c46459367cf888.pdf` | `id=341` `application_id=315` `exam_name=CET-6` `score_text=576` `certificate_attachment_url=/api/v1/portal/attachments/student-120/english_certificate/english_certificate-cff47ec45d7340f4a90bf11d23756b5d.pdf` |
| 第 2 行 | `id=2029` `application_id=315` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-120/english_certificate/english_certificate-e867457d5c154a0498c46459367cf888.pdf` | `id=342` `application_id=315` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-120/english_certificate/english_certificate-e867457d5c154a0498c46459367cf888.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270280

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1603` `application_id=316` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-584/english_certificate/english_certificate-db0267ecd87e4cd0975348d543c27dd0.pdf` | `id=343` `application_id=316` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-584/english_certificate/english_certificate-f6f5c22c13c349ef85930cb1c05771bf.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270281

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1398` `application_id=317` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-886/english_certificate/english_certificate-db0bf91b40104a4aa98c634fc3c69fde.pdf` | `id=344` `application_id=317` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-886/english_certificate/english_certificate-25837cbd3d764338a76c058df0029399.pdf` |
| 第 2 行 | `id=2030` `application_id=317` `exam_name=CET-6` `score_text=544` `certificate_attachment_url=/api/v1/portal/attachments/student-886/english_certificate/english_certificate-db0bf91b40104a4aa98c634fc3c69fde.pdf` | `id=345` `application_id=317` `exam_name=CET-6` `score_text=544` `certificate_attachment_url=/api/v1/portal/attachments/student-886/english_certificate/english_certificate-db0bf91b40104a4aa98c634fc3c69fde.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270288

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1594` `application_id=323` `exam_name=CET-6` `score_text=523` `certificate_attachment_url=/api/v1/portal/attachments/student-599/english_certificate/english_certificate-0708de60ff164f01a364b7066e84378e.pdf` | `id=353` `application_id=323` `exam_name=CET-6` `score_text=523` `certificate_attachment_url=/api/v1/portal/attachments/student-599/english_certificate/english_certificate-6bb607a4a9614765b8c4beac278b497b.pdf` |
| 第 2 行 | `id=2032` `application_id=323` `exam_name=其他` `score_text=606` `certificate_attachment_url=/api/v1/portal/attachments/student-599/english_certificate/english_certificate-0708de60ff164f01a364b7066e84378e.pdf` | `id=354` `application_id=323` `exam_name=其他` `score_text=606` `certificate_attachment_url=/api/v1/portal/attachments/student-599/english_certificate/english_certificate-0708de60ff164f01a364b7066e84378e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270289

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1099` `application_id=324` `exam_name=CET-6` `score_text=512` `certificate_attachment_url=/api/v1/portal/attachments/student-1308/english_certificate/english_certificate-0a92aa116acf49e695ab35d86c9d64d5.pdf` | `id=355` `application_id=324` `exam_name=CET-6` `score_text=512` `certificate_attachment_url=/api/v1/portal/attachments/student-1308/english_certificate/english_certificate-7e50224787ea474a8b8c56699a802cf9.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270299

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1402` `application_id=334` `exam_name=CET-6` `score_text=608` `certificate_attachment_url=/api/v1/portal/attachments/student-882/english_certificate/english_certificate-7c58a9ca7abd4f9195ff5773902deaa2.jpg` | `id=365` `application_id=334` `exam_name=CET-6` `score_text=608` `certificate_attachment_url=/api/v1/portal/attachments/student-882/english_certificate/english_certificate-0ea94a2db2b14f48a7ad88d2d90cb3f7.pdf` |
| 第 2 行 | `id=2033` `application_id=334` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-882/english_certificate/english_certificate-47517a3c248241d8ac0c1bfb2424a465.jpg` | `id=366` `application_id=334` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-882/english_certificate/english_certificate-47517a3c248241d8ac0c1bfb2424a465.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270300

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1737` `application_id=335` `exam_name=CET-6` `score_text=591` `certificate_attachment_url=/api/v1/portal/attachments/student-385/english_certificate/english_certificate-e8d153f0e9654197aafc101b2ee486f2.pdf` | `id=367` `application_id=335` `exam_name=CET-6` `score_text=591` `certificate_attachment_url=/api/v1/portal/attachments/student-385/english_certificate/english_certificate-473f3f1e5d3e48afa69e5de220f6cf40.pdf` |
| 第 2 行 | `id=2034` `application_id=335` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-385/english_certificate/english_certificate-e8d153f0e9654197aafc101b2ee486f2.pdf` | `id=368` `application_id=335` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-385/english_certificate/english_certificate-e8d153f0e9654197aafc101b2ee486f2.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270303

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1548` `application_id=338` `exam_name=CET-6` `score_text=486` `certificate_attachment_url=/api/v1/portal/attachments/student-670/english_certificate/english_certificate-8e7dc2d50be14ccfbbbcee1545a5ee6a.pdf` | `id=371` `application_id=338` `exam_name=CET-6` `score_text=486` `certificate_attachment_url=/api/v1/portal/attachments/student-670/english_certificate/english_certificate-6a9c714dd6ae49b28997a8cefc2d47c8.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270304

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1928` `application_id=339` `exam_name=CET-6` `score_text=624` `certificate_attachment_url=/api/v1/portal/attachments/student-79/english_certificate/english_certificate-cb9f64dfe30b40c487a466458fd5c726.pdf` | `id=372` `application_id=339` `exam_name=CET-6` `score_text=624` `certificate_attachment_url=/api/v1/portal/attachments/student-79/english_certificate/english_certificate-2c176ea328564486bf7eab2626c80197.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270307

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1560` `application_id=342` `exam_name=CET-6` `score_text=451` `certificate_attachment_url=/api/v1/portal/attachments/student-647/english_certificate/english_certificate-bff60f52137d4bc0bc379e6ebcb18df3.jpg` | `id=375` `application_id=342` `exam_name=CET-6` `score_text=451` `certificate_attachment_url=/api/v1/portal/attachments/student-647/english_certificate/english_certificate-94db369afe164a0f9d8cc88a7d67932c.jpg` |
| 第 2 行 | `id=2035` `application_id=342` `exam_name=其他` `score_text=483` `certificate_attachment_url=/api/v1/portal/attachments/student-647/english_certificate/english_certificate-bff60f52137d4bc0bc379e6ebcb18df3.jpg` | `id=376` `application_id=342` `exam_name=其他` `score_text=483` `certificate_attachment_url=/api/v1/portal/attachments/student-647/english_certificate/english_certificate-bff60f52137d4bc0bc379e6ebcb18df3.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270313

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1088` `application_id=348` `exam_name=CET-6` `score_text=520` `certificate_attachment_url=/api/v1/portal/attachments/student-1324/english_certificate/english_certificate-7bcf03db8c4f4110a0722f09d3a1f18a.jpg` | `id=382` `application_id=348` `exam_name=CET-6` `score_text=520` `certificate_attachment_url=/api/v1/portal/attachments/student-1324/english_certificate/english_certificate-91cd1b5e878c4bf483a3eabb65754c84.jpg` |
| 第 2 行 | `id=2036` `application_id=348` `exam_name=IELTS` `score_text=6.5（阅读7.5，听力7.5）` `certificate_attachment_url=/api/v1/portal/attachments/student-1324/english_certificate/english_certificate-7bcf03db8c4f4110a0722f09d3a1f18a.jpg` | `id=383` `application_id=348` `exam_name=IELTS` `score_text=6.5（阅读7.5，听力7.5）` `certificate_attachment_url=/api/v1/portal/attachments/student-1324/english_certificate/english_certificate-7bcf03db8c4f4110a0722f09d3a1f18a.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270314

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1726` `application_id=349` `exam_name=IELTS` `score_text=6.0` `certificate_attachment_url=/api/v1/portal/attachments/student-405/english_certificate/english_certificate-d54b2fa41d134cdfbd8f1acfd1e0aa45.pdf` | `id=384` `application_id=349` `exam_name=IELTS` `score_text=6.0` `certificate_attachment_url=/api/v1/portal/attachments/student-405/english_certificate/english_certificate-f8337c5a5a5c4a78a28fa3f51e037f5c.pdf` |
| 第 2 行 | `id=2037` `application_id=349` `exam_name=CET-6` `score_text=462` `certificate_attachment_url=/api/v1/portal/attachments/student-405/english_certificate/english_certificate-d54b2fa41d134cdfbd8f1acfd1e0aa45.pdf` | `id=385` `application_id=349` `exam_name=CET-6` `score_text=462` `certificate_attachment_url=/api/v1/portal/attachments/student-405/english_certificate/english_certificate-d54b2fa41d134cdfbd8f1acfd1e0aa45.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270318

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1269` `application_id=353` `exam_name=CET-6` `score_text=430` `certificate_attachment_url=/api/v1/portal/attachments/student-1061/english_certificate/english_certificate-3475d2400d054fc79197fbf446168e33.pdf` | `id=389` `application_id=353` `exam_name=CET-6` `score_text=430` `certificate_attachment_url=/api/v1/portal/attachments/student-1061/english_certificate/english_certificate-82c7322231284030854fc94ec9b7104f.pdf` |
| 第 2 行 | `id=2038` `application_id=353` `exam_name=其他` `score_text=483` `certificate_attachment_url=/api/v1/portal/attachments/student-1061/english_certificate/english_certificate-c04b0c207b0d474db3892cfc25043628.pdf` | `id=390` `application_id=353` `exam_name=其他` `score_text=483` `certificate_attachment_url=/api/v1/portal/attachments/student-1061/english_certificate/english_certificate-c04b0c207b0d474db3892cfc25043628.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270322

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1054` `application_id=357` `exam_name=CET-6` `score_text=636` `certificate_attachment_url=/api/v1/portal/attachments/student-1383/english_certificate/english_certificate-c7f55f5aaf7148f385437196af21ac02.pdf` | `id=395` `application_id=357` `exam_name=CET-6` `score_text=636` `certificate_attachment_url=/api/v1/portal/attachments/student-1383/english_certificate/english_certificate-b21ca01ca199488cbc367336915608ae.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270324

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1384` `application_id=359` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-902/english_certificate/english_certificate-b6dfc0f0e7864517b020163f724b02f1.pdf` | `id=397` `application_id=359` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-902/english_certificate/english_certificate-dae9f277a4064ca5a3f324b3f7311541.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270341

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1249` `application_id=377` `exam_name=CET-6` `score_text=608` `certificate_attachment_url=/api/v1/portal/attachments/student-1083/english_certificate/english_certificate-60718e0aa9e54b1a84caafc4a9ad7fec.pdf` | `id=415` `application_id=377` `exam_name=CET-6` `score_text=608` `certificate_attachment_url=/api/v1/portal/attachments/student-1083/english_certificate/english_certificate-77439dc320c04862abff39c417f48255.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270348

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1798` `application_id=384` `exam_name=CET-6` `score_text=508` `certificate_attachment_url=/api/v1/portal/attachments/student-270/english_certificate/english_certificate-314386540c4846ac843444baa9e622ba.pdf` | `id=422` `application_id=384` `exam_name=CET-6` `score_text=508` `certificate_attachment_url=/api/v1/portal/attachments/student-270/english_certificate/english_certificate-863947e164384f45baa893eec1cf5482.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270372

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1011` `application_id=407` `exam_name=CET-6` `score_text=590` `certificate_attachment_url=/api/v1/portal/attachments/student-1456/english_certificate/english_certificate-de2c72056b8b4b459470d6f207191397.pdf` | `id=447` `application_id=407` `exam_name=CET-6` `score_text=590` `certificate_attachment_url=/api/v1/portal/attachments/student-1456/english_certificate/english_certificate-81e12371e3f446048d4963f092c8809a.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270376

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1105` `application_id=410` `exam_name=CET-6` `score_text=589` `certificate_attachment_url=/api/v1/portal/attachments/student-1302/english_certificate/english_certificate-d3bd0dacf8f64a2595513d40c1501817.pdf` | `id=451` `application_id=410` `exam_name=CET-6` `score_text=589` `certificate_attachment_url=/api/v1/portal/attachments/student-1302/english_certificate/english_certificate-cb8638b3c08746f8b1bdb61b63f17275.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270382

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1250` `application_id=416` `exam_name=CET-6` `score_text=625` `certificate_attachment_url=/api/v1/portal/attachments/student-1082/english_certificate/english_certificate-fb575f6118884276a7de349a2c7477c9.pdf` | `id=457` `application_id=416` `exam_name=CET-6` `score_text=625` `certificate_attachment_url=/api/v1/portal/attachments/student-1082/english_certificate/english_certificate-7e7a032ba45f4a499061e6fb9ff111e7.pdf` |
| 第 2 行 | `id=2040` `application_id=416` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-1082/english_certificate/english_certificate-fb575f6118884276a7de349a2c7477c9.pdf` | `id=458` `application_id=416` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-1082/english_certificate/english_certificate-fb575f6118884276a7de349a2c7477c9.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270385

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1530` `application_id=256` `exam_name=CET-6` `score_text=491` `certificate_attachment_url=/api/v1/portal/attachments/student-698/english_certificate/english_certificate-9da6a604ca0e4d0fa088391142d7cd19.jpg` | `id=461` `application_id=256` `exam_name=CET-6` `score_text=491` `certificate_attachment_url=/api/v1/portal/attachments/student-698/english_certificate/english_certificate-264ca8bac76a4b60b682a627931b15e4.jpg` |
| 第 2 行 | `id=2041` `application_id=256` `exam_name=其他` `score_text=532` `certificate_attachment_url=/api/v1/portal/attachments/student-698/english_certificate/english_certificate-9da6a604ca0e4d0fa088391142d7cd19.jpg` | `id=462` `application_id=256` `exam_name=其他` `score_text=532` `certificate_attachment_url=/api/v1/portal/attachments/student-698/english_certificate/english_certificate-9da6a604ca0e4d0fa088391142d7cd19.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270386

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1729` `application_id=418` `exam_name=CET-6` `score_text=482` `certificate_attachment_url=/api/v1/portal/attachments/student-399/english_certificate/english_certificate-d1ccfe0f02204d019962b2a147a0d868.pdf` | `id=463` `application_id=418` `exam_name=CET-6` `score_text=482` `certificate_attachment_url=/api/v1/portal/attachments/student-399/english_certificate/english_certificate-9ab2e56fa4d940f498916c6d6a6699db.pdf` |
| 第 2 行 | `id=2042` `application_id=418` `exam_name=其他` `score_text=四级520` `certificate_attachment_url=/api/v1/portal/attachments/student-399/english_certificate/english_certificate-d1ccfe0f02204d019962b2a147a0d868.pdf` | `id=464` `application_id=418` `exam_name=其他` `score_text=四级520` `certificate_attachment_url=/api/v1/portal/attachments/student-399/english_certificate/english_certificate-d1ccfe0f02204d019962b2a147a0d868.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270390

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1679` `application_id=423` `exam_name=CET-6` `score_text=548` `certificate_attachment_url=/api/v1/portal/attachments/student-475/english_certificate/english_certificate-10ad4c4867274c219edc351b7b6e42a0.pdf` | `id=468` `application_id=423` `exam_name=CET-6` `score_text=548` `certificate_attachment_url=/api/v1/portal/attachments/student-475/english_certificate/english_certificate-31bd1df4e2b249a9ad802bfad62c2c73.pdf` |
| 第 2 行 | `id=2043` `application_id=423` `exam_name=TOEFL` `score_text=89` `certificate_attachment_url=/api/v1/portal/attachments/student-475/english_certificate/english_certificate-70736a1e449941f3bb56d291fd2e5dbc.pdf` | `id=469` `application_id=423` `exam_name=TOEFL` `score_text=89` `certificate_attachment_url=/api/v1/portal/attachments/student-475/english_certificate/english_certificate-70736a1e449941f3bb56d291fd2e5dbc.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270392

- 主库行数：1
- 备库行数：2
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1292` `application_id=425` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1034/english_certificate/english_certificate-3e59493c0d2f497783a4de12de1c17e8.pdf` | `id=1073` `application_id=425` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1034/english_certificate/english_certificate-6f7831bb39224b308e6a9d9cfd2f4729.pdf` |
| 第 2 行 | (missing) | `id=1074` `application_id=425` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1034/english_certificate/english_certificate-3e59493c0d2f497783a4de12de1c17e8.pdf` |

### candidate_no = SH20270395

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=985` `application_id=427` `exam_name=CET-6` `score_text=512` `certificate_attachment_url=/api/v1/portal/attachments/student-1496/english_certificate/english_certificate-ecbd734ccc4446b592ca7fbff6b26ef6.pdf` | `id=475` `application_id=427` `exam_name=CET-6` `score_text=512` `certificate_attachment_url=/api/v1/portal/attachments/student-1496/english_certificate/english_certificate-52bcdfc16bec447f993afce6eed459a1.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270399

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1058` `application_id=431` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1374/english_certificate/english_certificate-bc24a88fbe44478c873fd0e2d5ec39e6.pdf` | `id=479` `application_id=431` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1374/english_certificate/english_certificate-90e12804bc06452b804bca78245068e8.pdf` |
| 第 2 行 | `id=2044` `application_id=431` `exam_name=TOEFL` `score_text=109` `certificate_attachment_url=/api/v1/portal/attachments/student-1374/english_certificate/english_certificate-bc24a88fbe44478c873fd0e2d5ec39e6.pdf` | `id=480` `application_id=431` `exam_name=TOEFL` `score_text=109` `certificate_attachment_url=/api/v1/portal/attachments/student-1374/english_certificate/english_certificate-bc24a88fbe44478c873fd0e2d5ec39e6.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270402

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=953` `application_id=434` `exam_name=CET-6` `score_text=552` `certificate_attachment_url=/api/v1/portal/attachments/student-1549/english_certificate/english_certificate-00ce221a772b428894a6bda25e11d5d4.pdf` | `id=767` `application_id=434` `exam_name=CET-6` `score_text=552` `certificate_attachment_url=/api/v1/portal/attachments/student-1549/english_certificate/english_certificate-26f341018e2d4f8d954d9ee5cc2a3e54.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270417

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=937` `application_id=450` `exam_name=CET-6` `score_text=530` `certificate_attachment_url=/api/v1/portal/attachments/student-1579/english_certificate/english_certificate-f6d03e3783ef4f58a5aa7d2c8eb7707c.pdf` | `id=500` `application_id=450` `exam_name=CET-6` `score_text=530` `certificate_attachment_url=/api/v1/portal/attachments/student-1579/english_certificate/english_certificate-753a0df5a5e646c48943a35e27a1abbd.pdf` |
| 第 2 行 | `id=2046` `application_id=450` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1579/english_certificate/english_certificate-f6d03e3783ef4f58a5aa7d2c8eb7707c.pdf` | `id=501` `application_id=450` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1579/english_certificate/english_certificate-f6d03e3783ef4f58a5aa7d2c8eb7707c.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270424

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1894` `application_id=457` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-122/english_certificate/english_certificate-d16fbcf8e2a94bf09fe5527b25f56f96.pdf` | `id=508` `application_id=457` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-122/english_certificate/english_certificate-a6ef482c04bf423dbd29811110abdd8c.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270427

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=930` `application_id=460` `exam_name=CET-6` `score_text=508` `certificate_attachment_url=/api/v1/portal/attachments/student-1592/english_certificate/english_certificate-d16e08a89ca2488c8ee87ba58bf6a269.pdf` | `id=511` `application_id=460` `exam_name=CET-6` `score_text=508` `certificate_attachment_url=/api/v1/portal/attachments/student-1592/english_certificate/english_certificate-817a10165f5547af94fb95188aab2073.pdf` |
| 第 2 行 | `id=2047` `application_id=460` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1592/english_certificate/english_certificate-d16e08a89ca2488c8ee87ba58bf6a269.pdf` | `id=512` `application_id=460` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1592/english_certificate/english_certificate-d16e08a89ca2488c8ee87ba58bf6a269.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270430

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1366` `application_id=463` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-930/english_certificate/english_certificate-17cabf0f98d4409a816f6c777ba01810.jpg` | `id=515` `application_id=463` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-930/english_certificate/english_certificate-bbcbfa1d9d714968bc466fb42b460d6d.jpg` |
| 第 2 行 | `id=2048` `application_id=463` `exam_name=CET-6` `score_text=628` `certificate_attachment_url=/api/v1/portal/attachments/student-930/english_certificate/english_certificate-17cabf0f98d4409a816f6c777ba01810.jpg` | `id=516` `application_id=463` `exam_name=CET-6` `score_text=628` `certificate_attachment_url=/api/v1/portal/attachments/student-930/english_certificate/english_certificate-17cabf0f98d4409a816f6c777ba01810.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270438

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1457` `application_id=472` `exam_name=CET-6` `score_text=517` `certificate_attachment_url=/api/v1/portal/attachments/student-813/english_certificate/english_certificate-f46e4e4c9fb9479fae6e40de64e1e6f6.pdf` | `id=524` `application_id=472` `exam_name=CET-6` `score_text=517` `certificate_attachment_url=/api/v1/portal/attachments/student-813/english_certificate/english_certificate-17680844dd91424fa56940c27be030f4.pdf` |
| 第 2 行 | `id=2049` `application_id=472` `exam_name=TOEFL` `score_text=96` `certificate_attachment_url=/api/v1/portal/attachments/student-813/english_certificate/english_certificate-f46e4e4c9fb9479fae6e40de64e1e6f6.pdf` | `id=525` `application_id=472` `exam_name=TOEFL` `score_text=96` `certificate_attachment_url=/api/v1/portal/attachments/student-813/english_certificate/english_certificate-f46e4e4c9fb9479fae6e40de64e1e6f6.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270443

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1325` `application_id=477` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-989/english_certificate/english_certificate-741f328ca65d4d23bd76a190ed8e7dce.pdf` | `id=530` `application_id=477` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-989/english_certificate/english_certificate-69aabe0d4402463fb0d5d3b0a2217d98.pdf` |
| 第 2 行 | `id=2050` `application_id=477` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-989/english_certificate/english_certificate-741f328ca65d4d23bd76a190ed8e7dce.pdf` | `id=531` `application_id=477` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-989/english_certificate/english_certificate-741f328ca65d4d23bd76a190ed8e7dce.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270453

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=911` `application_id=487` `exam_name=CET-6` `score_text=565` `certificate_attachment_url=/api/v1/portal/attachments/student-1621/english_certificate/english_certificate-13a303e7df4a40bf8b9ece22edadea42.pdf` | `id=541` `application_id=487` `exam_name=CET-6` `score_text=565` `certificate_attachment_url=/api/v1/portal/attachments/student-1621/english_certificate/english_certificate-42d29a7031bc46eeb1b5e11c033661f2.pdf` |
| 第 2 行 | `id=2051` `application_id=487` `exam_name=TOEFL` `score_text=96` `certificate_attachment_url=/api/v1/portal/attachments/student-1621/english_certificate/english_certificate-13a303e7df4a40bf8b9ece22edadea42.pdf` | `id=542` `application_id=487` `exam_name=TOEFL` `score_text=96` `certificate_attachment_url=/api/v1/portal/attachments/student-1621/english_certificate/english_certificate-13a303e7df4a40bf8b9ece22edadea42.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270455

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1912` `application_id=488` `exam_name=CET-6` `score_text=587` `certificate_attachment_url=/api/v1/portal/attachments/student-99/english_certificate/english_certificate-17c7c9609935471bb8bf6e3bd644f0da.pdf` | `id=544` `application_id=488` `exam_name=CET-6` `score_text=587` `certificate_attachment_url=/api/v1/portal/attachments/student-99/english_certificate/english_certificate-40bbe103e6184d6ca105e458302cac78.pdf` |
| 第 2 行 | `id=1913` `application_id=488` `exam_name=TOEFL` `score_text=103` `certificate_attachment_url=/api/v1/portal/attachments/student-99/english_certificate/english_certificate-c3392432c0224072823cae35eae38ca4.pdf` | `id=545` `application_id=488` `exam_name=TOEFL` `score_text=103` `certificate_attachment_url=/api/v1/portal/attachments/student-99/english_certificate/english_certificate-c8c505d08642476a8f4fc01c9ee65d26.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270456

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1667` `application_id=489` `exam_name=CET-6` `score_text=531` `certificate_attachment_url=/api/v1/portal/attachments/student-493/english_certificate/english_certificate-7de5a456e2e14f5ab32c906d6c5d91d7.pdf` | `id=546` `application_id=489` `exam_name=CET-6` `score_text=531` `certificate_attachment_url=/api/v1/portal/attachments/student-493/english_certificate/english_certificate-4186656fe95e42a78be1e0abe13ab5bd.pdf` |
| 第 2 行 | `id=2052` `application_id=489` `exam_name=其他` `score_text=627` `certificate_attachment_url=/api/v1/portal/attachments/student-493/english_certificate/english_certificate-7de5a456e2e14f5ab32c906d6c5d91d7.pdf` | `id=547` `application_id=489` `exam_name=其他` `score_text=627` `certificate_attachment_url=/api/v1/portal/attachments/student-493/english_certificate/english_certificate-7de5a456e2e14f5ab32c906d6c5d91d7.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270459

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1750` `application_id=492` `exam_name=CET-6` `score_text=526` `certificate_attachment_url=/api/v1/portal/attachments/student-363/english_certificate/english_certificate-964b9ca8be194818bfa15ae27f500827.pdf` | `id=981` `application_id=492` `exam_name=CET-6` `score_text=526` `certificate_attachment_url=/api/v1/portal/attachments/student-363/english_certificate/english_certificate-7ac503d2ad5c4156ac6d93f38e4f08fc.pdf` |
| 第 2 行 | `id=2053` `application_id=492` `exam_name=其他` `score_text=627` `certificate_attachment_url=/api/v1/portal/attachments/student-363/english_certificate/english_certificate-964b9ca8be194818bfa15ae27f500827.pdf` | `id=982` `application_id=492` `exam_name=其他` `score_text=627` `certificate_attachment_url=/api/v1/portal/attachments/student-363/english_certificate/english_certificate-964b9ca8be194818bfa15ae27f500827.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270467

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1087` `application_id=500` `exam_name=CET-6` `score_text=581` `certificate_attachment_url=/api/v1/portal/attachments/student-1325/english_certificate/english_certificate-e1b8c02f6b164dcd81cf8b82a8dd64f1.pdf` | `id=559` `application_id=500` `exam_name=CET-6` `score_text=581` `certificate_attachment_url=/api/v1/portal/attachments/student-1325/english_certificate/english_certificate-31ae1f90a83947de861437c4a1d532de.pdf` |
| 第 2 行 | `id=2054` `application_id=500` `exam_name=IELTS` `score_text=7.0分（听 8.5/读 7.5/写 6.5/说 6）` `certificate_attachment_url=/api/v1/portal/attachments/student-1325/english_certificate/english_certificate-e1b8c02f6b164dcd81cf8b82a8dd64f1.pdf` | `id=560` `application_id=500` `exam_name=IELTS` `score_text=7.0分（听 8.5/读 7.5/写 6.5/说 6）` `certificate_attachment_url=/api/v1/portal/attachments/student-1325/english_certificate/english_certificate-e1b8c02f6b164dcd81cf8b82a8dd64f1.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270468

- 主库行数：2
- 备库行数：3
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=903` `application_id=501` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1639/english_certificate/english_certificate-48e4211257d542e49d1c88f4ac6f1fbe.pdf` | `id=561` `application_id=501` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1639/english_certificate/english_certificate-97f11a838d29485f90ef2d8879a9bf6c.pdf` |
| 第 2 行 | `id=2055` `application_id=501` `exam_name=CET-6` `score_text=583` `certificate_attachment_url=/api/v1/portal/attachments/student-1639/english_certificate/english_certificate-7ebae42b1e34455b8581332f5c23b179.pdf` | `id=562` `application_id=501` `exam_name=CET-6` `score_text=583` `certificate_attachment_url=/api/v1/portal/attachments/student-1639/english_certificate/english_certificate-7ebae42b1e34455b8581332f5c23b179.pdf` |
| 第 3 行 | (missing) | `id=563` `application_id=501` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1639/english_certificate/english_certificate-48e4211257d542e49d1c88f4ac6f1fbe.pdf` |

### candidate_no = SH20270473

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1879` `application_id=506` `exam_name=CET-6` `score_text=498` `certificate_attachment_url=/api/v1/portal/attachments/student-145/english_certificate/english_certificate-70ed99eec5b24e9797349f8e9145d3ec.png` | `id=568` `application_id=506` `exam_name=CET-6` `score_text=498` `certificate_attachment_url=/api/v1/portal/attachments/student-145/english_certificate/english_certificate-464731644aeb44c782ee7d03ec67a99c.png` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270480

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1526` `application_id=513` `exam_name=CET-6` `score_text=494` `certificate_attachment_url=/api/v1/portal/attachments/student-704/english_certificate/english_certificate-05be4c071f984a7fa74fbccab0926b9d.pdf` | `id=577` `application_id=513` `exam_name=CET-6` `score_text=494` `certificate_attachment_url=/api/v1/portal/attachments/student-704/english_certificate/english_certificate-ead6a615819b4715be37e6194b98a9c6.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270482

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1239` `application_id=515` `exam_name=CET-6` `score_text=613` `certificate_attachment_url=/api/v1/portal/attachments/student-1098/english_certificate/english_certificate-12894fb0b18648fa84d9e26ea7f8bbd3.pdf` | `id=1120` `application_id=515` `exam_name=CET-6` `score_text=613` `certificate_attachment_url=/api/v1/portal/attachments/student-1098/english_certificate/english_certificate-5781ef683b0d494790fb34cc18d658a0.pdf` |
| 第 2 行 | `id=2058` `application_id=515` `exam_name=TOEFL` `score_text=101` `certificate_attachment_url=/api/v1/portal/attachments/student-1098/english_certificate/english_certificate-12894fb0b18648fa84d9e26ea7f8bbd3.pdf` | `id=1121` `application_id=515` `exam_name=TOEFL` `score_text=101` `certificate_attachment_url=/api/v1/portal/attachments/student-1098/english_certificate/english_certificate-12894fb0b18648fa84d9e26ea7f8bbd3.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270486

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=885` `application_id=519` `exam_name=CET-6` `score_text=439` `certificate_attachment_url=/api/v1/portal/attachments/student-1680/english_certificate/english_certificate-66f204d81ca14c68906c2dc912f3af05.pdf` | `id=584` `application_id=519` `exam_name=CET-6` `score_text=439` `certificate_attachment_url=/api/v1/portal/attachments/student-1680/english_certificate/english_certificate-e71f168eb8a04b1abde345ada113c05f.pdf` |
| 第 2 行 | `id=2059` `application_id=519` `exam_name=IELTS` `score_text=6.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1680/english_certificate/english_certificate-66f204d81ca14c68906c2dc912f3af05.pdf` | `id=585` `application_id=519` `exam_name=IELTS` `score_text=6.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1680/english_certificate/english_certificate-66f204d81ca14c68906c2dc912f3af05.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270493

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1944` `application_id=526` `exam_name=TOEFL` `score_text=100` `certificate_attachment_url=/api/v1/portal/attachments/student-56/english_certificate/english_certificate-dec8ace94c4b4949af78eb958a881e23.pdf` | `id=592` `application_id=526` `exam_name=TOEFL` `score_text=100` `certificate_attachment_url=/api/v1/portal/attachments/student-56/english_certificate/english_certificate-4462eaa667a94bbdac3c3abc51241741.pdf` |
| 第 2 行 | `id=2060` `application_id=526` `exam_name=CET-6` `score_text=548` `certificate_attachment_url=/api/v1/portal/attachments/student-56/english_certificate/english_certificate-dec8ace94c4b4949af78eb958a881e23.pdf` | `id=593` `application_id=526` `exam_name=CET-6` `score_text=548` `certificate_attachment_url=/api/v1/portal/attachments/student-56/english_certificate/english_certificate-dec8ace94c4b4949af78eb958a881e23.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270500

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1176` `application_id=533` `exam_name=其他` `score_text=四级：606` `certificate_attachment_url=/api/v1/portal/attachments/student-1197/english_certificate/english_certificate-23a082cfa75b4b6bb145f9c0b461cf15.jpg` | `id=600` `application_id=533` `exam_name=其他` `score_text=四级：606` `certificate_attachment_url=/api/v1/portal/attachments/student-1197/english_certificate/english_certificate-3092ae40b5a04861b8fba7945aa20873.jpg` |
| 第 2 行 | `id=2061` `application_id=533` `exam_name=CET-6` `score_text=505` `certificate_attachment_url=/api/v1/portal/attachments/student-1197/english_certificate/english_certificate-23a082cfa75b4b6bb145f9c0b461cf15.jpg` | `id=601` `application_id=533` `exam_name=CET-6` `score_text=505` `certificate_attachment_url=/api/v1/portal/attachments/student-1197/english_certificate/english_certificate-23a082cfa75b4b6bb145f9c0b461cf15.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270504

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1215` `application_id=537` `exam_name=CET-6` `score_text=532` `certificate_attachment_url=/api/v1/portal/attachments/student-1131/english_certificate/english_certificate-8009ce6ec4844a44a260d4ec0a96f478.pdf` | `id=605` `application_id=537` `exam_name=CET-6` `score_text=532` `certificate_attachment_url=/api/v1/portal/attachments/student-1131/english_certificate/english_certificate-75a935799e1745269cb3fdb94aabd6af.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270506

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1124` `application_id=539` `exam_name=CET-6` `score_text=496` `certificate_attachment_url=/api/v1/portal/attachments/student-1278/english_certificate/english_certificate-a4ad0ce5b1c842ba92bbe3bda7338f58.pdf` | `id=607` `application_id=539` `exam_name=CET-6` `score_text=496` `certificate_attachment_url=/api/v1/portal/attachments/student-1278/english_certificate/english_certificate-ffe198a9b68848b987635f3e4dd8d683.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270511

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1981` `application_id=27` `exam_name=CET-6` `score_text=98` `certificate_attachment_url=/api/v1/portal/attachments/student-1/english_certificate/english_certificate-85db5937a51b45b79ce6216d2c03b2af.pdf` | `id=858` `application_id=27` `exam_name=CET-6` `score_text=98` `certificate_attachment_url=/api/v1/portal/attachments/student-1/english_certificate/english_certificate-e10beb3692034bfa8d06b7ed821b0d39.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270516

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1307` `application_id=552` `exam_name=CET-6` `score_text=504` `certificate_attachment_url=/api/v1/portal/attachments/student-1012/english_certificate/english_certificate-546b74caadf047c4adc9e48a9e4017e9.pdf` | `id=617` `application_id=552` `exam_name=CET-6` `score_text=504` `certificate_attachment_url=/api/v1/portal/attachments/student-1012/english_certificate/english_certificate-b44149eb9fff41898aff747c4e449179.pdf` |
| 第 2 行 | `id=2062` `application_id=552` `exam_name=其他` `score_text=547` `certificate_attachment_url=/api/v1/portal/attachments/student-1012/english_certificate/english_certificate-f8a4b949fbf14985b64a47e163ca4144.pdf` | `id=618` `application_id=552` `exam_name=其他` `score_text=547` `certificate_attachment_url=/api/v1/portal/attachments/student-1012/english_certificate/english_certificate-f8a4b949fbf14985b64a47e163ca4144.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270527

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=850` `application_id=563` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-1737/english_certificate/english_certificate-7c890692570840e69c2f255c189421c7.pdf` | `id=639` `application_id=563` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-1737/english_certificate/english_certificate-996c8d126a0443838837bf40b445709b.pdf` |
| 第 2 行 | `id=2063` `application_id=563` `exam_name=其他` `score_text=四级：615` `certificate_attachment_url=/api/v1/portal/attachments/student-1737/english_certificate/english_certificate-7c890692570840e69c2f255c189421c7.pdf` | `id=640` `application_id=563` `exam_name=其他` `score_text=四级：615` `certificate_attachment_url=/api/v1/portal/attachments/student-1737/english_certificate/english_certificate-7c890692570840e69c2f255c189421c7.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270531

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1763` `application_id=566` `exam_name=CET-6` `score_text=589` `certificate_attachment_url=/api/v1/portal/attachments/student-338/english_certificate/english_certificate-3e7ec6db55a5412cbd2124fc6cc96cb9.pdf` | `id=644` `application_id=566` `exam_name=CET-6` `score_text=589` `certificate_attachment_url=/api/v1/portal/attachments/student-338/english_certificate/english_certificate-8c8c454921764e40bfe65d4131bc327d.pdf` |
| 第 2 行 | `id=2064` `application_id=566` `exam_name=IELTS` `score_text=6` `certificate_attachment_url=/api/v1/portal/attachments/student-338/english_certificate/english_certificate-3e7ec6db55a5412cbd2124fc6cc96cb9.pdf` | `id=645` `application_id=566` `exam_name=IELTS` `score_text=6` `certificate_attachment_url=/api/v1/portal/attachments/student-338/english_certificate/english_certificate-3e7ec6db55a5412cbd2124fc6cc96cb9.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270532

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1903` `application_id=567` `exam_name=CET-6` `score_text=438` `certificate_attachment_url=/api/v1/portal/attachments/student-110/english_certificate/english_certificate-1aa56c28d1564b27aa33d26fc7788e77.pdf` | `id=646` `application_id=567` `exam_name=CET-6` `score_text=438` `certificate_attachment_url=/api/v1/portal/attachments/student-110/english_certificate/english_certificate-f2be6fcf4ef74108be50d44ab40d90f2.pdf` |
| 第 2 行 | `id=2065` `application_id=567` `exam_name=其他` `score_text=553` `certificate_attachment_url=/api/v1/portal/attachments/student-110/english_certificate/english_certificate-1aa56c28d1564b27aa33d26fc7788e77.pdf` | `id=647` `application_id=567` `exam_name=其他` `score_text=553` `certificate_attachment_url=/api/v1/portal/attachments/student-110/english_certificate/english_certificate-1aa56c28d1564b27aa33d26fc7788e77.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270541

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=844` `application_id=576` `exam_name=CET-6` `score_text=574` `certificate_attachment_url=/api/v1/portal/attachments/student-1750/english_certificate/english_certificate-39425688570148b5bf878ff46d0c57f5.pdf` | `id=656` `application_id=576` `exam_name=CET-6` `score_text=574` `certificate_attachment_url=/api/v1/portal/attachments/student-1750/english_certificate/english_certificate-d744713549ab42a48c00a79802741779.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270543

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=808` `application_id=578` `exam_name=CET-6` `score_text=458` `certificate_attachment_url=/api/v1/portal/attachments/student-1815/english_certificate/english_certificate-09d427c4b73344be94999c2b25c8ae41.pdf` | `id=658` `application_id=578` `exam_name=CET-6` `score_text=458` `certificate_attachment_url=/api/v1/portal/attachments/student-1815/english_certificate/english_certificate-528dbd12240f4e8a8c682734e036590a.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270549

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=976` `application_id=584` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1510/english_certificate/english_certificate-f6be9dd002ed459d8ee928419847227b.pdf` | `id=1209` `application_id=584` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1510/english_certificate/english_certificate-d0ef89b5d2104b16a8fd9e064c56d1df.pdf` |
| 第 2 行 | `id=2066` `application_id=584` `exam_name=CET-6` `score_text=510` `certificate_attachment_url=/api/v1/portal/attachments/student-1510/english_certificate/english_certificate-f6be9dd002ed459d8ee928419847227b.pdf` | `id=1210` `application_id=584` `exam_name=CET-6` `score_text=510` `certificate_attachment_url=/api/v1/portal/attachments/student-1510/english_certificate/english_certificate-f6be9dd002ed459d8ee928419847227b.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270555

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1668` `application_id=65` `exam_name=CET-6` `score_text=585` `certificate_attachment_url=/api/v1/portal/attachments/student-491/english_certificate/english_certificate-163e37f5e9964c3aa10d62a0ece06490.pdf` | `id=671` `application_id=65` `exam_name=CET-6` `score_text=585` `certificate_attachment_url=/api/v1/portal/attachments/student-491/english_certificate/english_certificate-193ab695e2e44f77b84cea531af38f67.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270564

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1052` `application_id=597` `exam_name=CET-6` `score_text=641` `certificate_attachment_url=/api/v1/portal/attachments/student-1386/english_certificate/english_certificate-4007e04687e64b1e8690b2f7d70c1f80.jpg` | `id=680` `application_id=597` `exam_name=CET-6` `score_text=641` `certificate_attachment_url=/api/v1/portal/attachments/student-1386/english_certificate/english_certificate-f6091589f4634f0db0b9363b092ee03a.png` |
| 第 2 行 | `id=2067` `application_id=597` `exam_name=其他` `score_text=全国大学生英语竞赛全国三等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-1386/english_certificate/english_certificate-4007e04687e64b1e8690b2f7d70c1f80.jpg` | `id=681` `application_id=597` `exam_name=其他` `score_text=全国大学生英语竞赛全国三等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-1386/english_certificate/english_certificate-4007e04687e64b1e8690b2f7d70c1f80.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270571

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1794` `application_id=604` `exam_name=CET-6` `score_text=545` `certificate_attachment_url=/api/v1/portal/attachments/student-280/english_certificate/english_certificate-1e4802ddccfb4bedbb885a81ec084856.pdf` | `id=688` `application_id=604` `exam_name=CET-6` `score_text=545` `certificate_attachment_url=/api/v1/portal/attachments/student-280/english_certificate/english_certificate-af1e58723f0646558f8e5f1771c5760d.pdf` |
| 第 2 行 | `id=2068` `application_id=604` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-280/english_certificate/english_certificate-1e4802ddccfb4bedbb885a81ec084856.pdf` | `id=689` `application_id=604` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-280/english_certificate/english_certificate-1e4802ddccfb4bedbb885a81ec084856.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270580

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1102` `application_id=613` `exam_name=CET-6` `score_text=689` `certificate_attachment_url=/api/v1/portal/attachments/student-1304/english_certificate/english_certificate-57345195857b48509ce51b79c1a13dcc.pdf` | `id=699` `application_id=613` `exam_name=CET-6` `score_text=689` `certificate_attachment_url=/api/v1/portal/attachments/student-1304/english_certificate/english_certificate-d54df384b3cb48049adb788faf80fa16.pdf` |
| 第 2 行 | `id=2070` `application_id=613` `exam_name=TOEFL` `score_text=110` `certificate_attachment_url=/api/v1/portal/attachments/student-1304/english_certificate/english_certificate-57345195857b48509ce51b79c1a13dcc.pdf` | `id=700` `application_id=613` `exam_name=TOEFL` `score_text=110` `certificate_attachment_url=/api/v1/portal/attachments/student-1304/english_certificate/english_certificate-57345195857b48509ce51b79c1a13dcc.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270585

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1184` `application_id=288` `exam_name=CET-6` `score_text=508` `certificate_attachment_url=/api/v1/portal/attachments/student-1184/english_certificate/english_certificate-0868b25148e14bd2b3a20b85ecb3b2b2.pdf` | `id=752` `application_id=288` `exam_name=CET-6` `score_text=508` `certificate_attachment_url=/api/v1/portal/attachments/student-1184/english_certificate/english_certificate-9efbd0667d7f4a0daf29ac9da2bc2da5.pdf` |
| 第 2 行 | `id=2071` `application_id=288` `exam_name=其他` `score_text=209` `certificate_attachment_url=/api/v1/portal/attachments/student-1184/english_certificate/english_certificate-0868b25148e14bd2b3a20b85ecb3b2b2.pdf` | `id=753` `application_id=288` `exam_name=其他` `score_text=209` `certificate_attachment_url=/api/v1/portal/attachments/student-1184/english_certificate/english_certificate-0868b25148e14bd2b3a20b85ecb3b2b2.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270594

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=791` `application_id=626` `exam_name=CET-6` `score_text=539` `certificate_attachment_url=/api/v1/portal/attachments/student-1834/english_certificate/english_certificate-889fe2bfe00941658ae53fc1593c85c6.pdf` | `id=1064` `application_id=626` `exam_name=CET-6` `score_text=539` `certificate_attachment_url=/api/v1/portal/attachments/student-1834/english_certificate/english_certificate-24906ef84e3249cb8723326859350ff0.pdf` |
| 第 2 行 | `id=2072` `application_id=626` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1834/english_certificate/english_certificate-883f4983e53d4513883d0a4577e37b2a.pdf` | `id=1065` `application_id=626` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1834/english_certificate/english_certificate-883f4983e53d4513883d0a4577e37b2a.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270600

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=825` `application_id=632` `exam_name=CET-6` `score_text=549` `certificate_attachment_url=/api/v1/portal/attachments/student-1785/english_certificate/english_certificate-78cc447dd7574a1e91684de956401406.pdf` | `id=723` `application_id=632` `exam_name=CET-6` `score_text=549` `certificate_attachment_url=/api/v1/portal/attachments/student-1785/english_certificate/english_certificate-95bc8ddcec0f4a1fa488efd8a9edc799.pdf` |
| 第 2 行 | `id=2074` `application_id=632` `exam_name=其他` `score_text=CET-4 611分` `certificate_attachment_url=/api/v1/portal/attachments/student-1785/english_certificate/english_certificate-78cc447dd7574a1e91684de956401406.pdf` | `id=724` `application_id=632` `exam_name=其他` `score_text=CET-4 611分` `certificate_attachment_url=/api/v1/portal/attachments/student-1785/english_certificate/english_certificate-78cc447dd7574a1e91684de956401406.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270601

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1002` `application_id=633` `exam_name=CET-6` `score_text=501` `certificate_attachment_url=/api/v1/portal/attachments/student-1469/english_certificate/english_certificate-0c16cb09a42947bda4ed203fdbbb7b06.pdf` | `id=725` `application_id=633` `exam_name=CET-6` `score_text=501` `certificate_attachment_url=/api/v1/portal/attachments/student-1469/english_certificate/english_certificate-fd79c23e794849ad8b75828b21a7590c.pdf` |
| 第 2 行 | `id=2075` `application_id=633` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1469/english_certificate/english_certificate-0c16cb09a42947bda4ed203fdbbb7b06.pdf` | `id=726` `application_id=633` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1469/english_certificate/english_certificate-0c16cb09a42947bda4ed203fdbbb7b06.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270605

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1343` `application_id=637` `exam_name=CET-6` `score_text=434` `certificate_attachment_url=/api/v1/portal/attachments/student-965/english_certificate/english_certificate-dcf47d1df65a4e69a3e1d542a91eabec.pdf` | `id=730` `application_id=637` `exam_name=CET-6` `score_text=434` `certificate_attachment_url=/api/v1/portal/attachments/student-965/english_certificate/english_certificate-0fd2f07e886e42ab99c6aa3ddfc8a9c0.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270607

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1160` `application_id=639` `exam_name=CET-6` `score_text=427` `certificate_attachment_url=/api/v1/portal/attachments/student-1220/english_certificate/english_certificate-8ade71ee86c442889d1ebbe6fbe30f75.pdf` | `id=732` `application_id=639` `exam_name=CET-6` `score_text=427` `certificate_attachment_url=/api/v1/portal/attachments/student-1220/english_certificate/english_certificate-81a085deee624dce891ad90a5f4eae19.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270608

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=743` `application_id=640` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1906/english_certificate/english_certificate-e5d53185516e40469d89ef7a338c37f6.pdf` | `id=733` `application_id=640` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1906/english_certificate/english_certificate-41e7f67bd4194bbd87a1d83b08c1d018.pdf` |
| 第 2 行 | `id=2076` `application_id=640` `exam_name=CET-6` `score_text=544` `certificate_attachment_url=/api/v1/portal/attachments/student-1906/english_certificate/english_certificate-e5d53185516e40469d89ef7a338c37f6.pdf` | `id=734` `application_id=640` `exam_name=CET-6` `score_text=544` `certificate_attachment_url=/api/v1/portal/attachments/student-1906/english_certificate/english_certificate-e5d53185516e40469d89ef7a338c37f6.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270614

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=819` `application_id=646` `exam_name=CET-6` `score_text=608` `certificate_attachment_url=/api/v1/portal/attachments/student-1797/english_certificate/english_certificate-3ba505c988a246b989a92f1ebc1c0ed3.pdf` | `id=740` `application_id=646` `exam_name=CET-6` `score_text=608` `certificate_attachment_url=/api/v1/portal/attachments/student-1797/english_certificate/english_certificate-1b1ac18f68704a9eae08b3b3b00ce582.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270623

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1419` `application_id=655` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-860/english_certificate/english_certificate-8e67bdc18de24b0688038e46324719ff.pdf` | `id=749` `application_id=655` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-860/english_certificate/english_certificate-dfa2a249a3e84a04b802be44eb194adc.pdf` |
| 第 2 行 | `id=2077` `application_id=655` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-860/english_certificate/english_certificate-8e67bdc18de24b0688038e46324719ff.pdf` | `id=750` `application_id=655` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-860/english_certificate/english_certificate-8e67bdc18de24b0688038e46324719ff.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270625

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1655` `application_id=657` `exam_name=CET-6` `score_text=538` `certificate_attachment_url=/api/v1/portal/attachments/student-510/english_certificate/english_certificate-ad69db2348db47d2b06cbfd2efb4257a.pdf` | `id=1101` `application_id=657` `exam_name=CET-6` `score_text=538` `certificate_attachment_url=/api/v1/portal/attachments/student-510/english_certificate/english_certificate-af7f06c8383e4d689cb3e91c89ec8e35.pdf` |
| 第 2 行 | `id=1656` `application_id=657` `exam_name=其他` `score_text=全国大学生英语竞赛三等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-510/english_certificate/english_certificate-87e89a6a2a1e4f5eb9035ce3202afc32.pdf` | `id=1102` `application_id=657` `exam_name=其他` `score_text=全国大学生英语竞赛三等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-510/english_certificate/english_certificate-9f38ea23526d44709eed7ce939e5e47f.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270638

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1922` `application_id=670` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-87/english_certificate/english_certificate-aa04f41a8c4b430281800af798ef2cc7.pdf` | `id=783` `application_id=670` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-87/english_certificate/english_certificate-dc99d548608c4b5a9ad0c14e0495dd32.pdf` |
| 第 2 行 | `id=2079` `application_id=670` `exam_name=CET-6` `score_text=536` `certificate_attachment_url=/api/v1/portal/attachments/student-87/english_certificate/english_certificate-aa04f41a8c4b430281800af798ef2cc7.pdf` | `id=784` `application_id=670` `exam_name=CET-6` `score_text=536` `certificate_attachment_url=/api/v1/portal/attachments/student-87/english_certificate/english_certificate-aa04f41a8c4b430281800af798ef2cc7.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270642

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1610` `application_id=674` `exam_name=CET-6` `score_text=610` `certificate_attachment_url=/api/v1/portal/attachments/student-573/english_certificate/english_certificate-f158a7c74d814c4587d7c980367eba96.pdf` | `id=789` `application_id=674` `exam_name=CET-6` `score_text=610` `certificate_attachment_url=/api/v1/portal/attachments/student-573/english_certificate/english_certificate-35be87f5d4804b359cef1fe167449a91.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270643

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1868` `application_id=675` `exam_name=CET-6` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-162/english_certificate/english_certificate-80dcba277a60401c8491e1b0f4847b50.pdf` | `id=792` `application_id=675` `exam_name=CET-6` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-162/english_certificate/english_certificate-3e4f8dcacff9454396a87bf8ed1f769a.pdf` |
| 第 2 行 | `id=2080` `application_id=675` `exam_name=其他` `score_text=606` `certificate_attachment_url=/api/v1/portal/attachments/student-162/english_certificate/english_certificate-80dcba277a60401c8491e1b0f4847b50.pdf` | `id=793` `application_id=675` `exam_name=其他` `score_text=606` `certificate_attachment_url=/api/v1/portal/attachments/student-162/english_certificate/english_certificate-80dcba277a60401c8491e1b0f4847b50.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270645

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1609` `application_id=677` `exam_name=CET-6` `score_text=500` `certificate_attachment_url=/api/v1/portal/attachments/student-577/english_certificate/english_certificate-cf2d3402cdf141baa015584830862cd1.pdf` | `id=795` `application_id=677` `exam_name=CET-6` `score_text=500` `certificate_attachment_url=/api/v1/portal/attachments/student-577/english_certificate/english_certificate-6df1401013034d35a9aed8476bcedbd4.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270648

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=888` `application_id=680` `exam_name=CET-6` `score_text=622` `certificate_attachment_url=/api/v1/portal/attachments/student-1674/english_certificate/english_certificate-a27c33219d2543bb8eb5e3f2b292d389.pdf` | `id=801` `application_id=680` `exam_name=CET-6` `score_text=622` `certificate_attachment_url=/api/v1/portal/attachments/student-1674/english_certificate/english_certificate-0fc253f4dc194785aaa155441e696332.pdf` |
| 第 2 行 | `id=2081` `application_id=680` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1674/english_certificate/english_certificate-34adfc9879d54bd0b8eee24a29a0bdd4.pdf` | `id=802` `application_id=680` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1674/english_certificate/english_certificate-34adfc9879d54bd0b8eee24a29a0bdd4.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270652

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1097` `application_id=684` `exam_name=CET-6` `score_text=567` `certificate_attachment_url=/api/v1/portal/attachments/student-1311/english_certificate/english_certificate-607309e89f2746cb810995d83ddbee0b.pdf` | `id=806` `application_id=684` `exam_name=CET-6` `score_text=567` `certificate_attachment_url=/api/v1/portal/attachments/student-1311/english_certificate/english_certificate-44f7dd9b353d4380bdfb035b84e62d58.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270667

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=942` `application_id=699` `exam_name=CET-6` `score_text=577` `certificate_attachment_url=/api/v1/portal/attachments/student-1574/english_certificate/english_certificate-0adeba14099c48afa3eee3e339d13aad.pdf` | `id=824` `application_id=699` `exam_name=CET-6` `score_text=577` `certificate_attachment_url=/api/v1/portal/attachments/student-1574/english_certificate/english_certificate-567698dbe0e44be89d631a318bbbc9ae.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270676

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1943` `application_id=708` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-57/english_certificate/english_certificate-31827f9b267a47ca8eb5856034a22bae.pdf` | `id=835` `application_id=708` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-57/english_certificate/english_certificate-367921d425de40398b706318f8f70589.pdf` |
| 第 2 行 | `id=2082` `application_id=708` `exam_name=CET-6` `score_text=549` `certificate_attachment_url=/api/v1/portal/attachments/student-57/english_certificate/english_certificate-31827f9b267a47ca8eb5856034a22bae.pdf` | `id=836` `application_id=708` `exam_name=CET-6` `score_text=549` `certificate_attachment_url=/api/v1/portal/attachments/student-57/english_certificate/english_certificate-31827f9b267a47ca8eb5856034a22bae.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270677

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1425` `application_id=709` `exam_name=CET-6` `score_text=492` `certificate_attachment_url=/api/v1/portal/attachments/student-854/english_certificate/english_certificate-c4e80e21e27742afae4c1fe711122069.pdf` | `id=837` `application_id=709` `exam_name=CET-6` `score_text=492` `certificate_attachment_url=/api/v1/portal/attachments/student-854/english_certificate/english_certificate-5caeea69ff1d479998bd1481d8f78859.pdf` |
| 第 2 行 | `id=2083` `application_id=709` `exam_name=其他` `score_text=583(英语四级)` `certificate_attachment_url=/api/v1/portal/attachments/student-854/english_certificate/english_certificate-c4e80e21e27742afae4c1fe711122069.pdf` | `id=838` `application_id=709` `exam_name=其他` `score_text=583(英语四级)` `certificate_attachment_url=/api/v1/portal/attachments/student-854/english_certificate/english_certificate-c4e80e21e27742afae4c1fe711122069.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270682

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=887` `application_id=714` `exam_name=CET-6` `score_text=545` `certificate_attachment_url=/api/v1/portal/attachments/student-1675/english_certificate/english_certificate-f033db18dff947fcbc421988b0b47d09.pdf` | `id=843` `application_id=714` `exam_name=CET-6` `score_text=545` `certificate_attachment_url=/api/v1/portal/attachments/student-1675/english_certificate/english_certificate-e77ee21768814b4d8421eb04ec81334c.pdf` |
| 第 2 行 | `id=2084` `application_id=714` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1675/english_certificate/english_certificate-f033db18dff947fcbc421988b0b47d09.pdf` | `id=844` `application_id=714` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1675/english_certificate/english_certificate-f033db18dff947fcbc421988b0b47d09.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270692

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1122` `application_id=724` `exam_name=CET-6` `score_text=623` `certificate_attachment_url=/api/v1/portal/attachments/student-1280/english_certificate/english_certificate-67848ee92943431d85f8c7dc197618d5.pdf` | `id=856` `application_id=724` `exam_name=CET-6` `score_text=623` `certificate_attachment_url=/api/v1/portal/attachments/student-1280/english_certificate/english_certificate-8567e3f028c14db3934dc7ee326447a3.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270694

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1033` `application_id=726` `exam_name=TOEFL` `score_text=105` `certificate_attachment_url=/api/v1/portal/attachments/student-1418/english_certificate/english_certificate-10f8352c2b8c4b7aa14cf7ddda34afa7.pdf` | `id=1058` `application_id=726` `exam_name=TOEFL` `score_text=105` `certificate_attachment_url=/api/v1/portal/attachments/student-1418/english_certificate/english_certificate-f7d7f790b971498dbca8f50a1bbfe268.pdf` |
| 第 2 行 | `id=2086` `application_id=726` `exam_name=CET-6` `score_text=556` `certificate_attachment_url=/api/v1/portal/attachments/student-1418/english_certificate/english_certificate-10f8352c2b8c4b7aa14cf7ddda34afa7.pdf` | `id=1059` `application_id=726` `exam_name=CET-6` `score_text=556` `certificate_attachment_url=/api/v1/portal/attachments/student-1418/english_certificate/english_certificate-10f8352c2b8c4b7aa14cf7ddda34afa7.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270697

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1287` `application_id=729` `exam_name=CET-6` `score_text=494` `certificate_attachment_url=/api/v1/portal/attachments/student-1040/english_certificate/english_certificate-b42013f421c14b7ebe55582fe3bc5b46.pdf` | `id=863` `application_id=729` `exam_name=CET-6` `score_text=494` `certificate_attachment_url=/api/v1/portal/attachments/student-1040/english_certificate/english_certificate-4fdea01492a54223bebb64d718678cc8.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270710

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=662` `application_id=742` `exam_name=IELTS` `score_text=7.5(7.5/9/6.5/6.5)` `certificate_attachment_url=/api/v1/portal/attachments/student-2051/english_certificate/english_certificate-62f88d591406424c93db97f4c4b28b25.pdf` | `id=876` `application_id=742` `exam_name=IELTS` `score_text=7.5(7.5/9/6.5/6.5)` `certificate_attachment_url=/api/v1/portal/attachments/student-2051/english_certificate/english_certificate-11a4ef77cc05418c9a727a699e02f315.pdf` |
| 第 2 行 | `id=2087` `application_id=742` `exam_name=CET-6` `score_text=621` `certificate_attachment_url=/api/v1/portal/attachments/student-2051/english_certificate/english_certificate-62f88d591406424c93db97f4c4b28b25.pdf` | `id=877` `application_id=742` `exam_name=CET-6` `score_text=621` `certificate_attachment_url=/api/v1/portal/attachments/student-2051/english_certificate/english_certificate-62f88d591406424c93db97f4c4b28b25.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270713

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1590` `application_id=745` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-607/english_certificate/english_certificate-a6c7fdf3f3c8460fa708156d84a48594.pdf` | `id=880` `application_id=745` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-607/english_certificate/english_certificate-af902e8488be4d45829bf7408fca6975.pdf` |
| 第 2 行 | `id=2088` `application_id=745` `exam_name=CET-6` `score_text=527` `certificate_attachment_url=/api/v1/portal/attachments/student-607/english_certificate/english_certificate-a6c7fdf3f3c8460fa708156d84a48594.pdf` | `id=881` `application_id=745` `exam_name=CET-6` `score_text=527` `certificate_attachment_url=/api/v1/portal/attachments/student-607/english_certificate/english_certificate-a6c7fdf3f3c8460fa708156d84a48594.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270715

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=914` `application_id=747` `exam_name=CET-6` `score_text=516` `certificate_attachment_url=/api/v1/portal/attachments/student-1615/english_certificate/english_certificate-72bceaaf051c45d3836244b5f5d5cddb.pdf` | `id=883` `application_id=747` `exam_name=CET-6` `score_text=516` `certificate_attachment_url=/api/v1/portal/attachments/student-1615/english_certificate/english_certificate-0a225fee3cb54e078b601d4f9d42a8a1.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270719

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1435` `application_id=751` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-844/english_certificate/english_certificate-e0f6cb7c5ae547759cd52f25af58697f.jpg` | `id=887` `application_id=751` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-844/english_certificate/english_certificate-4ab5a55222a8460d950b95c1049ecb9e.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270721

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=620` `application_id=753` `exam_name=CET-6` `score_text=524` `certificate_attachment_url=/api/v1/portal/attachments/student-2118/english_certificate/english_certificate-1d55f943b050443d8e4176dd48c7d78e.pdf` | `id=889` `application_id=753` `exam_name=CET-6` `score_text=524` `certificate_attachment_url=/api/v1/portal/attachments/student-2118/english_certificate/english_certificate-5d4fcaf3bdf2464c822dc82b00b759bf.pdf` |
| 第 2 行 | `id=2089` `application_id=753` `exam_name=其他` `score_text=英语四级602` `certificate_attachment_url=/api/v1/portal/attachments/student-2118/english_certificate/english_certificate-1d55f943b050443d8e4176dd48c7d78e.pdf` | `id=890` `application_id=753` `exam_name=其他` `score_text=英语四级602` `certificate_attachment_url=/api/v1/portal/attachments/student-2118/english_certificate/english_certificate-1d55f943b050443d8e4176dd48c7d78e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270727

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=799` `application_id=759` `exam_name=CET-6` `score_text=551` `certificate_attachment_url=/api/v1/portal/attachments/student-1825/english_certificate/english_certificate-f829d83a36494b499703a7c49460a2ad.pdf` | `id=897` `application_id=759` `exam_name=CET-6` `score_text=551` `certificate_attachment_url=/api/v1/portal/attachments/student-1825/english_certificate/english_certificate-3ee9d28708db4d39a41c7e7784e217ab.pdf` |
| 第 2 行 | `id=2090` `application_id=759` `exam_name=其他` `score_text=CET4 641` `certificate_attachment_url=/api/v1/portal/attachments/student-1825/english_certificate/english_certificate-f829d83a36494b499703a7c49460a2ad.pdf` | `id=898` `application_id=759` `exam_name=其他` `score_text=CET4 641` `certificate_attachment_url=/api/v1/portal/attachments/student-1825/english_certificate/english_certificate-f829d83a36494b499703a7c49460a2ad.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270745

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=747` `application_id=777` `exam_name=CET-6` `score_text=483` `certificate_attachment_url=/api/v1/portal/attachments/student-1897/english_certificate/english_certificate-dc4c0045f5b2471bb55d7cef72cae530.pdf` | `id=917` `application_id=777` `exam_name=CET-6` `score_text=483` `certificate_attachment_url=/api/v1/portal/attachments/student-1897/english_certificate/english_certificate-f11820cd354d4ede8304245215166d56.pdf` |
| 第 2 行 | `id=2091` `application_id=777` `exam_name=其他` `score_text=620` `certificate_attachment_url=/api/v1/portal/attachments/student-1897/english_certificate/english_certificate-dc4c0045f5b2471bb55d7cef72cae530.pdf` | `id=918` `application_id=777` `exam_name=其他` `score_text=620` `certificate_attachment_url=/api/v1/portal/attachments/student-1897/english_certificate/english_certificate-dc4c0045f5b2471bb55d7cef72cae530.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270750

- 主库行数：3
- 备库行数：3
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1321` `application_id=782` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-994/english_certificate/english_certificate-4885a278cf6749da92546dc0342f2a59.jpg` | `id=923` `application_id=782` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-994/english_certificate/english_certificate-113fb50c184f455a88312ee0b3c31db8.jpg` |
| 第 2 行 | `id=2092` `application_id=782` `exam_name=CET-6` `score_text=571` `certificate_attachment_url=/api/v1/portal/attachments/student-994/english_certificate/english_certificate-9f5ab790b6b740e29710d3e44bbbe335.jpg` | `id=924` `application_id=782` `exam_name=CET-6` `score_text=571` `certificate_attachment_url=/api/v1/portal/attachments/student-994/english_certificate/english_certificate-9f5ab790b6b740e29710d3e44bbbe335.jpg` |
| 第 3 行 | `id=2093` `application_id=782` `exam_name=其他` `score_text=639` `certificate_attachment_url=/api/v1/portal/attachments/student-994/english_certificate/english_certificate-4885a278cf6749da92546dc0342f2a59.jpg` | `id=925` `application_id=782` `exam_name=其他` `score_text=639` `certificate_attachment_url=/api/v1/portal/attachments/student-994/english_certificate/english_certificate-4885a278cf6749da92546dc0342f2a59.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270752

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=920` `application_id=784` `exam_name=CET-6` `score_text=538` `certificate_attachment_url=/api/v1/portal/attachments/student-1606/english_certificate/english_certificate-840ea492eee040b388d61241b78e878f.pdf` | `id=927` `application_id=784` `exam_name=CET-6` `score_text=538` `certificate_attachment_url=/api/v1/portal/attachments/student-1606/english_certificate/english_certificate-99242dec0a5d46dc86ec24a7d95d398a.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270756

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=737` `application_id=788` `exam_name=CET-6` `score_text=565` `certificate_attachment_url=/api/v1/portal/attachments/student-1917/english_certificate/english_certificate-f81a2a607aa0445b82369f65d5437483.pdf` | `id=931` `application_id=788` `exam_name=CET-6` `score_text=565` `certificate_attachment_url=/api/v1/portal/attachments/student-1917/english_certificate/english_certificate-b324bbb45d474a929fd1304de68412d6.pdf` |
| 第 2 行 | `id=2094` `application_id=788` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1917/english_certificate/english_certificate-c3807905e3254cddb3ed880c60c054e8.pdf` | `id=932` `application_id=788` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1917/english_certificate/english_certificate-c3807905e3254cddb3ed880c60c054e8.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270761

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=684` `application_id=793` `exam_name=CET-6` `score_text=564` `certificate_attachment_url=/api/v1/portal/attachments/student-2014/english_certificate/english_certificate-06127f9fceef46cd8835298f536ca975.pdf` | `id=937` `application_id=793` `exam_name=CET-6` `score_text=564` `certificate_attachment_url=/api/v1/portal/attachments/student-2014/english_certificate/english_certificate-d0be2a94d58c47eb879581cca31e8ba8.pdf` |
| 第 2 行 | `id=2095` `application_id=793` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-2014/english_certificate/english_certificate-06127f9fceef46cd8835298f536ca975.pdf` | `id=938` `application_id=793` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-2014/english_certificate/english_certificate-06127f9fceef46cd8835298f536ca975.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270766

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=842` `application_id=798` `exam_name=CET-6` `score_text=580` `certificate_attachment_url=/api/v1/portal/attachments/student-1753/english_certificate/english_certificate-1a9c84ae4e6c41b098206eea8906ff0d.pdf` | `id=943` `application_id=798` `exam_name=CET-6` `score_text=580` `certificate_attachment_url=/api/v1/portal/attachments/student-1753/english_certificate/english_certificate-39eea3988dd54f66ad2b9bc5f45c14eb.jpg` |
| 第 2 行 | `id=2096` `application_id=798` `exam_name=TOEFL` `score_text=102` `certificate_attachment_url=/api/v1/portal/attachments/student-1753/english_certificate/english_certificate-1a9c84ae4e6c41b098206eea8906ff0d.pdf` | `id=944` `application_id=798` `exam_name=TOEFL` `score_text=102` `certificate_attachment_url=/api/v1/portal/attachments/student-1753/english_certificate/english_certificate-1a9c84ae4e6c41b098206eea8906ff0d.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270770

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=606` `application_id=802` `exam_name=CET-6` `score_text=561` `certificate_attachment_url=/api/v1/portal/attachments/student-2144/english_certificate/english_certificate-52a958ff26a44834b3c2d7656cdcd990.pdf` | `id=1197` `application_id=802` `exam_name=CET-6` `score_text=561` `certificate_attachment_url=/api/v1/portal/attachments/student-2144/english_certificate/english_certificate-6e36572b60e3498484e4bd3823de8f28.pdf` |
| 第 2 行 | `id=2097` `application_id=802` `exam_name=其他` `score_text=624` `certificate_attachment_url=/api/v1/portal/attachments/student-2144/english_certificate/english_certificate-52a958ff26a44834b3c2d7656cdcd990.pdf` | `id=1198` `application_id=802` `exam_name=其他` `score_text=624` `certificate_attachment_url=/api/v1/portal/attachments/student-2144/english_certificate/english_certificate-52a958ff26a44834b3c2d7656cdcd990.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270771

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1020` `application_id=803` `exam_name=CET-6` `score_text=432` `certificate_attachment_url=/api/v1/portal/attachments/student-1442/english_certificate/english_certificate-6b7fbffec24f4dcda41770e36a1117b7.pdf` | `id=951` `application_id=803` `exam_name=CET-6` `score_text=432` `certificate_attachment_url=/api/v1/portal/attachments/student-1442/english_certificate/english_certificate-917b1b860f414ec4bb07230c13eae0d4.pdf` |
| 第 2 行 | `id=2098` `application_id=803` `exam_name=其他` `score_text=521` `certificate_attachment_url=/api/v1/portal/attachments/student-1442/english_certificate/english_certificate-aab38b9f387d4f6c9391d78231cd86dd.pdf` | `id=952` `application_id=803` `exam_name=其他` `score_text=521` `certificate_attachment_url=/api/v1/portal/attachments/student-1442/english_certificate/english_certificate-aab38b9f387d4f6c9391d78231cd86dd.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270781

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1883` `application_id=813` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-141/english_certificate/english_certificate-3f24feea63c04a319ec72ecd17900d9e.pdf` | `id=969` `application_id=813` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-141/english_certificate/english_certificate-05a7784bb4074438aef9127402c52b1a.jpg` |
| 第 2 行 | `id=2099` `application_id=813` `exam_name=CET-6` `score_text=563` `certificate_attachment_url=/api/v1/portal/attachments/student-141/english_certificate/english_certificate-3f24feea63c04a319ec72ecd17900d9e.pdf` | `id=970` `application_id=813` `exam_name=CET-6` `score_text=563` `certificate_attachment_url=/api/v1/portal/attachments/student-141/english_certificate/english_certificate-3f24feea63c04a319ec72ecd17900d9e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270794

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1607` `application_id=826` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-580/english_certificate/english_certificate-35428d4aabf34125afab0f06a6f493a5.pdf` | `id=991` `application_id=826` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-580/english_certificate/english_certificate-db92f3dc66cb4a5382a116bb97b72971.jpg` |
| 第 2 行 | `id=2100` `application_id=826` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-580/english_certificate/english_certificate-35428d4aabf34125afab0f06a6f493a5.pdf` | `id=992` `application_id=826` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-580/english_certificate/english_certificate-35428d4aabf34125afab0f06a6f493a5.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270797

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1661` `application_id=829` `exam_name=CET-6` `score_text=618` `certificate_attachment_url=/api/v1/portal/attachments/student-503/english_certificate/english_certificate-e4c8edda827d48df9d9360bd0f63a569.pdf` | `id=997` `application_id=829` `exam_name=CET-6` `score_text=618` `certificate_attachment_url=/api/v1/portal/attachments/student-503/english_certificate/english_certificate-784f923fe9654d628f3c6a610c6529fd.pdf` |
| 第 2 行 | `id=2101` `application_id=829` `exam_name=其他` `score_text=671` `certificate_attachment_url=/api/v1/portal/attachments/student-503/english_certificate/english_certificate-e4c8edda827d48df9d9360bd0f63a569.pdf` | `id=998` `application_id=829` `exam_name=其他` `score_text=671` `certificate_attachment_url=/api/v1/portal/attachments/student-503/english_certificate/english_certificate-e4c8edda827d48df9d9360bd0f63a569.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270799

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=570` `application_id=831` `exam_name=CET-6` `score_text=637` `certificate_attachment_url=/api/v1/portal/attachments/student-2204/english_certificate/english_certificate-5e41f21c5c4e412b8a2071d47dff0580.pdf` | `id=1000` `application_id=831` `exam_name=CET-6` `score_text=637` `certificate_attachment_url=/api/v1/portal/attachments/student-2204/english_certificate/english_certificate-68877beac8754071aa0c0490161a76ff.pdf` |
| 第 2 行 | `id=2102` `application_id=831` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-2204/english_certificate/english_certificate-5e41f21c5c4e412b8a2071d47dff0580.pdf` | `id=1001` `application_id=831` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-2204/english_certificate/english_certificate-5e41f21c5c4e412b8a2071d47dff0580.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270810

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=880` `application_id=842` `exam_name=CET-6` `score_text=647` `certificate_attachment_url=/api/v1/portal/attachments/student-1695/english_certificate/english_certificate-873007eff60146f98e7bc3621d62c607.png` | `id=1016` `application_id=842` `exam_name=CET-6` `score_text=647` `certificate_attachment_url=/api/v1/portal/attachments/student-1695/english_certificate/english_certificate-673e8f59b6464fdf8f4e406809e0b953.png` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270816

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=656` `application_id=848` `exam_name=CET-6` `score_text=560` `certificate_attachment_url=/api/v1/portal/attachments/student-2061/english_certificate/english_certificate-956f956a87c94bebbaf265a919daaf8f.pdf` | `id=1023` `application_id=848` `exam_name=CET-6` `score_text=560` `certificate_attachment_url=/api/v1/portal/attachments/student-2061/english_certificate/english_certificate-749f1215624d4a6582569d93c924bdf8.pdf` |
| 第 2 行 | `id=2103` `application_id=848` `exam_name=其他` `score_text=全国大学生英语竞赛三等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-2061/english_certificate/english_certificate-956f956a87c94bebbaf265a919daaf8f.pdf` | `id=1024` `application_id=848` `exam_name=其他` `score_text=全国大学生英语竞赛三等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-2061/english_certificate/english_certificate-956f956a87c94bebbaf265a919daaf8f.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270823

- 主库行数：1
- 备库行数：2
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=561` `application_id=855` `exam_name=其他` `score_text=英授证明` `certificate_attachment_url=/api/v1/portal/attachments/student-2218/english_certificate/english_certificate-25757ad3af7f4867b8715ce6eafcfc52.png` | `id=1033` `application_id=855` `exam_name=其他` `score_text=四级500` `certificate_attachment_url=/api/v1/portal/attachments/student-2218/english_certificate/english_certificate-25757ad3af7f4867b8715ce6eafcfc52.png` |
| 第 2 行 | (missing) | `id=1034` `application_id=855` `exam_name=其他` `score_text=英授证明` `certificate_attachment_url=/api/v1/portal/attachments/student-2218/english_certificate/english_certificate-1317df947263431bbe3d16b8b357ae51.pdf` |

### candidate_no = SH20270826

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1466` `application_id=858` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-796/english_certificate/english_certificate-8263acbb51d14513b24e94d95e88fb3d.pdf` | `id=1040` `application_id=858` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-796/english_certificate/english_certificate-fc53757d34ea4bb49ff62ccaf22cdeda.jpg` |
| 第 2 行 | `id=2105` `application_id=858` `exam_name=CET-6` `score_text=493` `certificate_attachment_url=/api/v1/portal/attachments/student-796/english_certificate/english_certificate-8263acbb51d14513b24e94d95e88fb3d.pdf` | `id=1041` `application_id=858` `exam_name=CET-6` `score_text=493` `certificate_attachment_url=/api/v1/portal/attachments/student-796/english_certificate/english_certificate-8263acbb51d14513b24e94d95e88fb3d.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270832

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=546` `application_id=864` `exam_name=CET-6` `score_text=595` `certificate_attachment_url=/api/v1/portal/attachments/student-2239/english_certificate/english_certificate-b4907a2c904949b6af41612e49bddc5d.jpg` | `id=1048` `application_id=864` `exam_name=CET-6` `score_text=595` `certificate_attachment_url=/api/v1/portal/attachments/student-2239/english_certificate/english_certificate-1d5f9ae99f994187ad4c68388215831f.pdf` |
| 第 2 行 | `id=2106` `application_id=864` `exam_name=其他` `score_text=全国大学生英语词汇能力大赛山东赛区一等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-2239/english_certificate/english_certificate-b4907a2c904949b6af41612e49bddc5d.jpg` | `id=1049` `application_id=864` `exam_name=其他` `score_text=全国大学生英语词汇能力大赛山东赛区一等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-2239/english_certificate/english_certificate-b4907a2c904949b6af41612e49bddc5d.jpg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270843

- 主库行数：1
- 备库行数：1
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=576` `application_id=875` `exam_name=CET-6` `score_text=491` `certificate_attachment_url=/api/v1/portal/attachments/student-2191/english_certificate/english_certificate-04b3de4ff7b8466b8418cbfac395e0d6.pdf` | `id=1080` `application_id=875` `exam_name=CET-6` `score_text=491` `certificate_attachment_url=/api/v1/portal/attachments/student-2191/english_certificate/english_certificate-460f18a9e8e04c6da406cefeb58362a2.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270862

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=599` `application_id=894` `exam_name=CET-6` `score_text=577` `certificate_attachment_url=/api/v1/portal/attachments/student-2150/english_certificate/english_certificate-5b10c83dcd204a528068c531386447e2.jpeg` | `id=1107` `application_id=894` `exam_name=CET-6` `score_text=577` `certificate_attachment_url=/api/v1/portal/attachments/student-2150/english_certificate/english_certificate-eedeb396d54c4d639c8738d85617c0de.pdf` |
| 第 2 行 | `id=2108` `application_id=894` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-2150/english_certificate/english_certificate-5b10c83dcd204a528068c531386447e2.jpeg` | `id=1108` `application_id=894` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-2150/english_certificate/english_certificate-5b10c83dcd204a528068c531386447e2.jpeg` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270870

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=894` `application_id=902` `exam_name=CET-6` `score_text=432` `certificate_attachment_url=/api/v1/portal/attachments/student-1659/english_certificate/english_certificate-7122ec51fdec4ba197fe49b1d894585b.pdf` | `id=1118` `application_id=902` `exam_name=CET-6` `score_text=432` `certificate_attachment_url=/api/v1/portal/attachments/student-1659/english_certificate/english_certificate-9cb74302d2d74c7a9d37b1aaed373f40.pdf` |
| 第 2 行 | `id=2109` `application_id=902` `exam_name=TOEFL` `score_text=88` `certificate_attachment_url=/api/v1/portal/attachments/student-1659/english_certificate/english_certificate-7122ec51fdec4ba197fe49b1d894585b.pdf` | `id=1119` `application_id=902` `exam_name=TOEFL` `score_text=88` `certificate_attachment_url=/api/v1/portal/attachments/student-1659/english_certificate/english_certificate-7122ec51fdec4ba197fe49b1d894585b.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270883

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1778` `application_id=915` `exam_name=CET-6` `score_text=643` `certificate_attachment_url=/api/v1/portal/attachments/student-310/english_certificate/english_certificate-d01079078fa94148a215b8af746e5da8.pdf` | `id=1139` `application_id=915` `exam_name=CET-6` `score_text=643` `certificate_attachment_url=/api/v1/portal/attachments/student-310/english_certificate/english_certificate-373a71ad58af4cbc808cddf19f86e752.pdf` |
| 第 2 行 | `id=2110` `application_id=915` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-310/english_certificate/english_certificate-e72541d131cf4cb98a97d4e6c9bd8e6b.pdf` | `id=1140` `application_id=915` `exam_name=IELTS` `score_text=7` `certificate_attachment_url=/api/v1/portal/attachments/student-310/english_certificate/english_certificate-e72541d131cf4cb98a97d4e6c9bd8e6b.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270892

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=499` `application_id=924` `exam_name=CET-6` `score_text=579` `certificate_attachment_url=/api/v1/portal/attachments/student-2305/english_certificate/english_certificate-04edea1b27ce4c9b8158f46827c67d49.pdf` | `id=1151` `application_id=924` `exam_name=CET-6` `score_text=579` `certificate_attachment_url=/api/v1/portal/attachments/student-2305/english_certificate/english_certificate-d99e6cb6927548d8b6fa434b53098a76.pdf` |
| 第 2 行 | `id=2111` `application_id=924` `exam_name=其他` `score_text=622` `certificate_attachment_url=/api/v1/portal/attachments/student-2305/english_certificate/english_certificate-04edea1b27ce4c9b8158f46827c67d49.pdf` | `id=1152` `application_id=924` `exam_name=其他` `score_text=622` `certificate_attachment_url=/api/v1/portal/attachments/student-2305/english_certificate/english_certificate-04edea1b27ce4c9b8158f46827c67d49.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270894

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1768` `application_id=926` `exam_name=CET-6` `score_text=586` `certificate_attachment_url=/api/v1/portal/attachments/student-329/english_certificate/english_certificate-3a51e30c1ed640d38dda98c7a88770b0.pdf` | `id=1157` `application_id=926` `exam_name=CET-6` `score_text=586` `certificate_attachment_url=/api/v1/portal/attachments/student-329/english_certificate/english_certificate-c368f28a70b5420da3b52cdb354147d8.pdf` |
| 第 2 行 | `id=2112` `application_id=926` `exam_name=TOEFL` `score_text=104` `certificate_attachment_url=/api/v1/portal/attachments/student-329/english_certificate/english_certificate-3a51e30c1ed640d38dda98c7a88770b0.pdf` | `id=1158` `application_id=926` `exam_name=TOEFL` `score_text=104` `certificate_attachment_url=/api/v1/portal/attachments/student-329/english_certificate/english_certificate-3a51e30c1ed640d38dda98c7a88770b0.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270896

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=527` `application_id=928` `exam_name=CET-6` `score_text=578` `certificate_attachment_url=/api/v1/portal/attachments/student-2264/english_certificate/english_certificate-2f67e5732d9f47c798e5ff7a8387ca8e.pdf` | `id=1161` `application_id=928` `exam_name=CET-6` `score_text=578` `certificate_attachment_url=/api/v1/portal/attachments/student-2264/english_certificate/english_certificate-970fd22430524ce88848ffaba3a993a6.pdf` |
| 第 2 行 | `id=2113` `application_id=928` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-2264/english_certificate/english_certificate-2f67e5732d9f47c798e5ff7a8387ca8e.pdf` | `id=1162` `application_id=928` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-2264/english_certificate/english_certificate-2f67e5732d9f47c798e5ff7a8387ca8e.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270904

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=692` `application_id=936` `exam_name=CET-6` `score_text=643` `certificate_attachment_url=/api/v1/portal/attachments/student-1998/english_certificate/english_certificate-4d307149ecac405892f33ffc336be3e1.pdf` | `id=1175` `application_id=936` `exam_name=CET-6` `score_text=643` `certificate_attachment_url=/api/v1/portal/attachments/student-1998/english_certificate/english_certificate-482a2a9435524ddc9fccb5cd76ad0081.pdf` |
| 第 2 行 | `id=2114` `application_id=936` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1998/english_certificate/english_certificate-4d307149ecac405892f33ffc336be3e1.pdf` | `id=1176` `application_id=936` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1998/english_certificate/english_certificate-4d307149ecac405892f33ffc336be3e1.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270916

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1491` `application_id=948` `exam_name=CET-6` `score_text=677` `certificate_attachment_url=/api/v1/portal/attachments/student-757/english_certificate/english_certificate-22db1d8b54024b78943a3950c5ec9d52.png` | `id=1195` `application_id=948` `exam_name=CET-6` `score_text=677` `certificate_attachment_url=/api/v1/portal/attachments/student-757/english_certificate/english_certificate-610baa15532b491fb2b37efc44f83aae.png` |
| 第 2 行 | `id=2115` `application_id=948` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-757/english_certificate/english_certificate-22db1d8b54024b78943a3950c5ec9d52.png` | `id=1196` `application_id=948` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-757/english_certificate/english_certificate-22db1d8b54024b78943a3950c5ec9d52.png` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270919

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1773` `application_id=951` `exam_name=CET-6` `score_text=608` `certificate_attachment_url=/api/v1/portal/attachments/student-320/english_certificate/english_certificate-f12216e468a74494a7360646e251ee24.pdf` | `id=1202` `application_id=951` `exam_name=CET-6` `score_text=608` `certificate_attachment_url=/api/v1/portal/attachments/student-320/english_certificate/english_certificate-38dbe94e628e4e20b88f363687c1835c.pdf` |
| 第 2 行 | `id=2116` `application_id=951` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-320/english_certificate/english_certificate-f12216e468a74494a7360646e251ee24.pdf` | `id=1203` `application_id=951` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-320/english_certificate/english_certificate-f12216e468a74494a7360646e251ee24.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270920

- 主库行数：2
- 备库行数：2
- 附件 URL 是否一致：否

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=481` `application_id=952` `exam_name=CET-6` `score_text=566` `certificate_attachment_url=/api/v1/portal/attachments/student-2336/english_certificate/english_certificate-4982e426eec34694a0875e7b0231185b.pdf` | `id=1204` `application_id=952` `exam_name=CET-6` `score_text=566` `certificate_attachment_url=/api/v1/portal/attachments/student-2336/english_certificate/english_certificate-63e45f27cc9b4d92bc90d79c7737957a.pdf` |
| 第 2 行 | `id=2117` `application_id=952` `exam_name=TOEFL` `score_text=100` `certificate_attachment_url=/api/v1/portal/attachments/student-2336/english_certificate/english_certificate-4982e426eec34694a0875e7b0231185b.pdf` | `id=1205` `application_id=952` `exam_name=TOEFL` `score_text=100` `certificate_attachment_url=/api/v1/portal/attachments/student-2336/english_certificate/english_certificate-4982e426eec34694a0875e7b0231185b.pdf` |

> 说明：本组 candidate_no 的 exam_name / score_text 已匹配一致，但 certificate_attachment_url 不同，已单独标记。

### candidate_no = SH20270924

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1157` `application_id=956` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1224/english_certificate/english_certificate-71793701170a4d68b262cd5c2774f4ab.jpg` | (missing) |

### candidate_no = SH20270925

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1299` `application_id=957` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1025/english_certificate/english_certificate-88e43cafd1a449a6a58091f2270c5891.pdf` | (missing) |

### candidate_no = SH20270926

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1739` `application_id=958` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-381/english_certificate/english_certificate-90535fdf111843c087a98ecb55eb0d42.pdf` | (missing) |

### candidate_no = SH20270927

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1145` `application_id=959` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1246/english_certificate/english_certificate-538bf578f50548fd8b85cf68fefcdfe7.pdf` | (missing) |

### candidate_no = SH20270928

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=518` `application_id=960` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2277/english_certificate/english_certificate-e0a4d9062060499382fa0d26efe2b636.pdf` | (missing) |

### candidate_no = SH20270929

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=536` `application_id=961` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2252/english_certificate/english_certificate-3afa828e02374069b69f6f98eee456df.pdf` | (missing) |

### candidate_no = SH20270930

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=841` `application_id=962` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1755/english_certificate/english_certificate-d5f4d1f8d59d447eb250a23b166f1386.pdf` | (missing) |

### candidate_no = SH20270931

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1426` `application_id=963` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-853/english_certificate/english_certificate-e440b61569d445278e89d817b314f6fd.pdf` | (missing) |

### candidate_no = SH20270932

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1132` `application_id=964` `exam_name=CET-6` `score_text=500` `certificate_attachment_url=/api/v1/portal/attachments/student-1266/english_certificate/english_certificate-4f6544c762da4f318b2040dc739eb87c.pdf` | (missing) |
| 第 2 行 | `id=1133` `application_id=964` `exam_name=IELTS` `score_text=6` `certificate_attachment_url=/api/v1/portal/attachments/student-1266/english_certificate/english_certificate-7ef2e3687db64f45887e39215ead0df1.pdf` | (missing) |

### candidate_no = SH20270933

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1643` `application_id=965` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-525/english_certificate/english_certificate-3b95cfcb89874f409c9c052aa88ddde6.pdf` | (missing) |

### candidate_no = SH20270934

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=897` `application_id=966` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1653/english_certificate/english_certificate-eec7d957ee9746bf96b6c0d4008c4c81.pdf` | (missing) |

### candidate_no = SH20270935

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=533` `application_id=967` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2256/english_certificate/english_certificate-2bb5f90eea444a13aa65f1c0f5578357.pdf` | (missing) |

### candidate_no = SH20270936

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=557` `application_id=968` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2226/english_certificate/english_certificate-2fdada3941f24cb189ee9fd65eb9cb91.pdf` | (missing) |

### candidate_no = SH20270937

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=521` `application_id=969` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2274/english_certificate/english_certificate-93e0ced54f0b4333b8baa4687001b388.pdf` | (missing) |

### candidate_no = SH20270938

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=452` `application_id=970` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2381/english_certificate/english_certificate-1991a4f826334577bf273f94a98d384f.png` | (missing) |

### candidate_no = SH20270939

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1219` `application_id=971` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1126/english_certificate/english_certificate-7027942693b94528b259150f62d3230e.pdf` | (missing) |

### candidate_no = SH20270940

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=488` `application_id=972` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2324/english_certificate/english_certificate-85387104052346c9a8b14783d5d4399e.pdf` | (missing) |

### candidate_no = SH20270941

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=443` `application_id=973` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2392/english_certificate/english_certificate-5ae07ad94050401a853555afbc1d1594.pdf` | (missing) |

### candidate_no = SH20270942

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=954` `application_id=974` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1547/english_certificate/english_certificate-b66f68e49b0246eb93b189f25262e9ae.pdf` | (missing) |

### candidate_no = SH20270943

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1030` `application_id=975` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1426/english_certificate/english_certificate-3c11900d99dc4a86a7c92cebfd41ca76.pdf` | (missing) |

### candidate_no = SH20270944

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1423` `application_id=976` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-856/english_certificate/english_certificate-e1e6adccc9af4418b9d7b05628fa30c3.pdf` | (missing) |

### candidate_no = SH20270945

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1204` `application_id=977` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1147/english_certificate/english_certificate-e3f92116b2a347daabe6ab0b799105bd.pdf` | (missing) |

### candidate_no = SH20270946

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=879` `application_id=978` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1696/english_certificate/english_certificate-25b77753c2414d6daa61b925a3251bee.pdf` | (missing) |

### candidate_no = SH20270947

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=665` `application_id=979` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2047/english_certificate/english_certificate-ba08219075ef42bc8bd25dda3e5ad535.pdf` | (missing) |

### candidate_no = SH20270948

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1177` `application_id=980` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1196/english_certificate/english_certificate-da4bb51420b94bcd820a55e64eb751c1.pdf` | (missing) |

### candidate_no = SH20270949

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=980` `application_id=981` `exam_name=CET-6` `score_text=577` `certificate_attachment_url=/api/v1/portal/attachments/student-1504/english_certificate/english_certificate-dff713bc5be54b3888dbe0805f67ca7e.pdf` | (missing) |

### candidate_no = SH20270950

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1470` `application_id=982` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-790/english_certificate/english_certificate-453cef66a8a34c249b67c0204c2469e0.pdf` | (missing) |

### candidate_no = SH20270951

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=436` `application_id=983` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2402/english_certificate/english_certificate-1919414159394473b60e3ba2a9e3e91f.pdf` | (missing) |

### candidate_no = SH20270952

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1146` `application_id=984` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1245/english_certificate/english_certificate-52c17dfd2cd24bb0b73bc8a9a1951c40.pdf` | (missing) |

### candidate_no = SH20270953

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=483` `application_id=985` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2332/english_certificate/english_certificate-fc938c6b501540129136d7794e73a887.pdf` | (missing) |

### candidate_no = SH20270954

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1182` `application_id=986` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1187/english_certificate/english_certificate-f4ec86dbae6146c0988c25ed55d52db3.png` | (missing) |

### candidate_no = SH20270955

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1150` `application_id=987` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1239/english_certificate/english_certificate-7ec99451eebe4aaea0f3ecc676eaa1c5.pdf` | (missing) |

### candidate_no = SH20270956

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1658` `application_id=988` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-508/english_certificate/english_certificate-c2d53d637a7347fbb70b87737d0b6ccf.pdf` | (missing) |

### candidate_no = SH20270957

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=435` `application_id=989` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2404/english_certificate/english_certificate-1737cb397ebc484fb3b20df63dfb21cb.pdf` | (missing) |

### candidate_no = SH20270958

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1621` `application_id=990` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-556/english_certificate/english_certificate-55ca55a48f6744ce95289dfa883ce4cc.pdf` | (missing) |

### candidate_no = SH20270959

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1353` `application_id=991` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-947/english_certificate/english_certificate-018e1b763c1a419eb5e9353c94161178.pdf` | (missing) |

### candidate_no = SH20270960

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=440` `application_id=992` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2395/english_certificate/english_certificate-96be39fb1a4148cba7c0c946549a2fb8.pdf` | (missing) |

### candidate_no = SH20270961

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=978` `application_id=993` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1506/english_certificate/english_certificate-23d797f84bbf4ecaa7450aafec9683ee.pdf` | (missing) |

### candidate_no = SH20270962

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1616` `application_id=994` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-565/english_certificate/english_certificate-b9ad54cc8c344b4c90c5a55027d12c4f.pdf` | (missing) |

### candidate_no = SH20270963

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=972` `application_id=995` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1516/english_certificate/english_certificate-d2b13750fd854374abfabe61f6d926fb.pdf` | (missing) |

### candidate_no = SH20270964

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=430` `application_id=996` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2412/english_certificate/english_certificate-69133b361ad640c09c4d63c6214c44fa.pdf` | (missing) |

### candidate_no = SH20270965

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1513` `application_id=997` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-726/english_certificate/english_certificate-a5f241026bd84080ac8d55ea5f24f736.pdf` | (missing) |

### candidate_no = SH20270966

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1583` `application_id=998` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-615/english_certificate/english_certificate-f6407eea0e594777ac426bb32da1c072.pdf` | (missing) |

### candidate_no = SH20270967

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=477` `application_id=999` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2344/english_certificate/english_certificate-20d5b2634f54405fbf0598641310a337.png` | (missing) |

### candidate_no = SH20270968

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1388` `application_id=1000` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-897/english_certificate/english_certificate-64f0f245ffe8437db2616f44be686cf6.pdf` | (missing) |

### candidate_no = SH20270969

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1487` `application_id=1001` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-765/english_certificate/english_certificate-eb66417c83484750ac8b9168d2dd4c9a.pdf` | (missing) |

### candidate_no = SH20270970

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=432` `application_id=1002` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2408/english_certificate/english_certificate-62745d968da54cf6bb96211d46d0076b.pdf` | (missing) |

### candidate_no = SH20270971

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1577` `application_id=1003` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-624/english_certificate/english_certificate-3b7e0a520df242a48251e2aabae29263.pdf` | (missing) |

### candidate_no = SH20270972

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=549` `application_id=1004` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2236/english_certificate/english_certificate-f2361f1bc3954900875cda6dd9cc63ef.pdf` | (missing) |

### candidate_no = SH20270973

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=702` `application_id=1005` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1975/english_certificate/english_certificate-d45c2a18156b45d8944d95f88b7a7c4d.pdf` | (missing) |

### candidate_no = SH20270974

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=429` `application_id=1006` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2418/english_certificate/english_certificate-817ff60b08184f949360f5b467d12256.pdf` | (missing) |

### candidate_no = SH20270975

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=514` `application_id=1007` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2282/english_certificate/english_certificate-a259807783c44e8e9384863c41865155.pdf` | (missing) |

### candidate_no = SH20270976

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=416` `application_id=1008` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2450/english_certificate/english_certificate-a2aa3caa68bf4560b722adc27d0c5a54.pdf` | (missing) |

### candidate_no = SH20270977

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1770` `application_id=1009` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-326/english_certificate/english_certificate-73119d472f484ccf8f69d87321b08f60.pdf` | (missing) |

### candidate_no = SH20270978

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=637` `application_id=1010` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2088/english_certificate/english_certificate-92336b98b5034b5f85d886cef7f88afc.jpg` | (missing) |

### candidate_no = SH20270979

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=604` `application_id=1011` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2146/english_certificate/english_certificate-e555175a37df4ae38e998f8c89cd5e5f.pdf` | (missing) |

### candidate_no = SH20270980

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=449` `application_id=1012` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2385/english_certificate/english_certificate-1b38a61165194f7187f6905d3a2bc629.pdf` | (missing) |

### candidate_no = SH20270981

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=412` `application_id=1013` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2460/english_certificate/english_certificate-fd3c52fbe32e4548855f26a44c6327f2.pdf` | (missing) |

### candidate_no = SH20270982

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=428` `application_id=1014` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2421/english_certificate/english_certificate-51af4f0c60ec48abb8ca49367cbbffa7.pdf` | (missing) |

### candidate_no = SH20270983

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1178` `application_id=1015` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1195/english_certificate/english_certificate-93b19a3698e44b13be5e3a1f950e6a87.pdf` | (missing) |

### candidate_no = SH20270984

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=864` `application_id=1016` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1715/english_certificate/english_certificate-b44c810a0f3c4a099001ac0717d559c3.pdf` | (missing) |

### candidate_no = SH20270985

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=607` `application_id=1017` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2143/english_certificate/english_certificate-8498e2891e0e450a837bbf63c5e0056b.png` | (missing) |

### candidate_no = SH20270986

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1917` `application_id=1018` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-95/english_certificate/english_certificate-cb50fcc00a3244d2a2e493da6121cd1d.pdf` | (missing) |

### candidate_no = SH20270987

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=721` `application_id=1019` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1941/english_certificate/english_certificate-68c8087b5eb14a21a65dbe3f0c269d09.pdf` | (missing) |

### candidate_no = SH20270988

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1216` `application_id=1020` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1129/english_certificate/english_certificate-af7b747ccd8b46248a4e4584c37d6bce.pdf` | (missing) |

### candidate_no = SH20270989

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=413` `application_id=1021` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2456/english_certificate/english_certificate-abb0fd5e764e4ae7bbd202c4f1359f17.pdf` | (missing) |

### candidate_no = SH20270990

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1311` `application_id=1022` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1007/english_certificate/english_certificate-597bd99f2eb84cc28b2518caf822548e.png` | (missing) |

### candidate_no = SH20270991

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1508` `application_id=1023` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-735/english_certificate/english_certificate-a85650283987442a824519cd1a8ff079.pdf` | (missing) |

### candidate_no = SH20270992

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=495` `application_id=1024` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2312/english_certificate/english_certificate-f16b9c8246dd407c9f80c3e99e0ab339.pdf` | (missing) |

### candidate_no = SH20270993

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1504` `application_id=1025` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-743/english_certificate/english_certificate-ff2e517267fd4006b369d1faccdcf410.pdf` | (missing) |

### candidate_no = SH20270994

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=425` `application_id=1026` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2428/english_certificate/english_certificate-aa8876b7f9644f2f8aa63647f0003953.pdf` | (missing) |

### candidate_no = SH20270995

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=922` `application_id=1027` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1603/english_certificate/english_certificate-668db0cbd5c74259b0cf326071f03829.jpg` | (missing) |

### candidate_no = SH20270996

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=386` `application_id=1028` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2511/english_certificate/english_certificate-bea1409f181749c0a35f321f818a782e.pdf` | (missing) |

### candidate_no = SH20270997

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1357` `application_id=1029` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-942/english_certificate/english_certificate-9e7a5961cbcd47ff8cdd5b45e73f7fb9.jpg` | (missing) |

### candidate_no = SH20270998

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=484` `application_id=1030` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2329/english_certificate/english_certificate-47aa507ecaaa49c9967b12debaf06ee6.pdf` | (missing) |

### candidate_no = SH20270999

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=402` `application_id=1031` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2482/english_certificate/english_certificate-520f6c76c23e48e4b8dd98c89b82395c.pdf` | (missing) |

### candidate_no = SH20271000

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=460` `application_id=1032` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2368/english_certificate/english_certificate-d4c1c8bcde3f4e088e14d4076bd19023.pdf` | (missing) |

### candidate_no = SH20271001

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1375` `application_id=1033` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-914/english_certificate/english_certificate-7682eab7b98e44bb8e221bdf7d57bb88.pdf` | (missing) |

### candidate_no = SH20271002

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=385` `application_id=1034` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2512/english_certificate/english_certificate-8666acaa69ed47d9801ab90f3766eceb.pdf` | (missing) |

### candidate_no = SH20271003

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1580` `application_id=1035` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-621/english_certificate/english_certificate-3e47e288c0704d47a5e6f3301942d218.pdf` | (missing) |

### candidate_no = SH20271004

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1306` `application_id=1036` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1013/english_certificate/english_certificate-db03e2459c6e45a596b9f155349e3992.pdf` | (missing) |

### candidate_no = SH20271005

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=397` `application_id=1037` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2491/english_certificate/english_certificate-886f3afbf43646dc898b4ff236c7de72.png` | (missing) |

### candidate_no = SH20271006

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1807` `application_id=1038` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-254/english_certificate/english_certificate-78827e98f4994b7bb0c8400c8eafdc89.pdf` | (missing) |

### candidate_no = SH20271007

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=837` `application_id=1039` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1762/english_certificate/english_certificate-46823037aba54c5e81cfdc917331df0f.pdf` | (missing) |

### candidate_no = SH20271008

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=461` `application_id=1040` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2367/english_certificate/english_certificate-d8cde6e768f74097ad0dca81637f5c69.pdf` | (missing) |

### candidate_no = SH20271009

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1754` `application_id=1041` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-355/english_certificate/english_certificate-c9c395ac681d43a0ae76ac41337756c2.pdf` | (missing) |

### candidate_no = SH20271010

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=388` `application_id=1042` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2506/english_certificate/english_certificate-02bf6f8e344b4fe98878c6749f54f10f.pdf` | (missing) |

### candidate_no = SH20271011

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1064` `application_id=1043` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1364/english_certificate/english_certificate-5df8183e43744b12a7c89f6e577d859f.pdf` | (missing) |

### candidate_no = SH20271012

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=676` `application_id=1044` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2029/english_certificate/english_certificate-0e8722cc0bc54a8481d0bcb5df001c11.pdf` | (missing) |

### candidate_no = SH20271013

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1874` `application_id=1045` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-154/english_certificate/english_certificate-da5447a30caf43339dbb82fcb72cd727.pdf` | (missing) |

### candidate_no = SH20271014

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1604` `application_id=1046` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-583/english_certificate/english_certificate-44113af19d58432599914b68437223d3.pdf` | (missing) |

### candidate_no = SH20271015

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=938` `application_id=1047` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1578/english_certificate/english_certificate-02153c2e9c8e496b963869c9d610f383.pdf` | (missing) |

### candidate_no = SH20271016

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=373` `application_id=1048` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2539/english_certificate/english_certificate-04f559a1c2a0472fa8377ee7de47be17.pdf` | (missing) |

### candidate_no = SH20271017

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1496` `application_id=1049` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-752/english_certificate/english_certificate-c51e7c0cfbc64bd1b3c116d104eb7ff2.pdf` | (missing) |

### candidate_no = SH20271018

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=371` `application_id=1050` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2541/english_certificate/english_certificate-147f00bcb2a049f59cf81a61d01cb94d.pdf` | (missing) |

### candidate_no = SH20271019

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1069` `application_id=1051` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1355/english_certificate/english_certificate-9734a88bee9340da81724b50c966d9f5.pdf` | (missing) |

### candidate_no = SH20271020

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1374` `application_id=1052` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-917/english_certificate/english_certificate-9429e471eba445af892e554020acb3d1.pdf` | (missing) |

### candidate_no = SH20271021

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1478` `application_id=1053` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-776/english_certificate/english_certificate-bb15e24b3ddf4695bb0fa64beb7b92c2.png` | (missing) |

### candidate_no = SH20271022

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=404` `application_id=1054` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2479/english_certificate/english_certificate-44ccb48c280147149a3c4a9aab52375d.pdf` | (missing) |

### candidate_no = SH20271023

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=372` `application_id=1055` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2540/english_certificate/english_certificate-99e2df7226c74067b6ec5248050dccc6.pdf` | (missing) |

### candidate_no = SH20271024

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=779` `application_id=1056` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1848/english_certificate/english_certificate-d23a991e85ea424f94af234907dd1fb3.pdf` | (missing) |

### candidate_no = SH20271025

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1442` `application_id=1057` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-834/english_certificate/english_certificate-9e1cfd7536974555855321c4d9f24202.pdf` | (missing) |

### candidate_no = SH20271026

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=384` `application_id=1058` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2515/english_certificate/english_certificate-0e83ff10e7b047d4b421451d39041d87.pdf` | (missing) |

### candidate_no = SH20271027

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=439` `application_id=1059` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2399/english_certificate/english_certificate-441ed1d7ec714e23a9641626e5ce632b.pdf` | (missing) |

### candidate_no = SH20271028

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=812` `application_id=1060` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1810/english_certificate/english_certificate-b8f81cb07ecc432886136cbf420e6dd7.pdf` | (missing) |

### candidate_no = SH20271029

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=542` `application_id=1061` `exam_name=CET-6` `score_text=516` `certificate_attachment_url=/api/v1/portal/attachments/student-2244/english_certificate/english_certificate-c2f63636e1c94a098286ba48712fd863.pdf` | (missing) |

### candidate_no = SH20271030

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=855` `application_id=1062` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1726/english_certificate/english_certificate-401f94a49b3d4ec483e3fc2361f74bf0.pdf` | (missing) |

### candidate_no = SH20271031

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=691` `application_id=1063` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2000/english_certificate/english_certificate-0a945e5ba5c3423697cb16510727e4d4.pdf` | (missing) |

### candidate_no = SH20271032

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=401` `application_id=1064` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2485/english_certificate/english_certificate-df87f897f5c8430eb5911dd745fbb2ab.pdf` | (missing) |

### candidate_no = SH20271033

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=823` `application_id=1065` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1791/english_certificate/english_certificate-dc95ae8223c246f3b96a99defc25744c.pdf` | (missing) |

### candidate_no = SH20271034

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1327` `application_id=1066` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-984/english_certificate/english_certificate-044fa7e2359341a3830ebda7092d8519.pdf` | (missing) |

### candidate_no = SH20271035

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=359` `application_id=1067` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2563/english_certificate/english_certificate-c808a979a4f841c9ade45d3f2b2e981c.pdf` | (missing) |

### candidate_no = SH20271036

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=355` `application_id=1068` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2567/english_certificate/english_certificate-6e554435ae4d461a90608ee1670b28d6.pdf` | (missing) |

### candidate_no = SH20271037

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=357` `application_id=1069` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2565/english_certificate/english_certificate-6cf8ad66f8ea43c69e2fec971d06974f.jpg` | (missing) |

### candidate_no = SH20271038

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1781` `application_id=1070` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-301/english_certificate/english_certificate-8fcfc73d94244beb84a4cc58300e3412.png` | (missing) |

### candidate_no = SH20271039

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=473` `application_id=1071` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2349/english_certificate/english_certificate-16b075b97fdd4527aa7d41b087644f18.pdf` | (missing) |

### candidate_no = SH20271040

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1297` `application_id=1072` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1028/english_certificate/english_certificate-7aa18935720440d49fba0d20780280d3.pdf` | (missing) |

### candidate_no = SH20271041

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=509` `application_id=1073` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2292/english_certificate/english_certificate-589c2f8495a5492c9fd3dc18a3517645.pdf` | (missing) |

### candidate_no = SH20271042

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1623` `application_id=1074` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-554/english_certificate/english_certificate-8342d0b9b9d742c8b3e239a306cd37bf.pdf` | (missing) |

### candidate_no = SH20271043

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=883` `application_id=1075` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1684/english_certificate/english_certificate-82afd87f285c47fda64be568305f531f.pdf` | (missing) |

### candidate_no = SH20271044

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1093` `application_id=1076` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1315/english_certificate/english_certificate-b83822e29731455c960244c2fb9936ef.pdf` | (missing) |

### candidate_no = SH20271045

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=568` `application_id=1077` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2206/english_certificate/english_certificate-bab5fe2354f54890a314c5a2bec6836c.pdf` | (missing) |

### candidate_no = SH20271046

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1045` `application_id=1078` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1395/english_certificate/english_certificate-b13b03b12eb44f938632471a5c1ba2f4.pdf` | (missing) |

### candidate_no = SH20271047

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=609` `application_id=1079` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2138/english_certificate/english_certificate-c311bfcb693f4edfa3629b7f12d7bfb0.pdf` | (missing) |

### candidate_no = SH20271048

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1324` `application_id=1080` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-990/english_certificate/english_certificate-69dcdbe750724d8e9e9352d7fda3a52c.pdf` | (missing) |

### candidate_no = SH20271049

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=356` `application_id=1081` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2566/english_certificate/english_certificate-d8b6f5bc1f2f4c53999c72fd3246c733.pdf` | (missing) |

### candidate_no = SH20271050

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=594` `application_id=1082` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2162/english_certificate/english_certificate-f37019218c8c4a579f3e127a94bc0cd5.pdf` | (missing) |

### candidate_no = SH20271051

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=360` `application_id=1083` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2562/english_certificate/english_certificate-44873b979d5a47a8a6a75112e1473566.pdf` | (missing) |

### candidate_no = SH20271052

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=715` `application_id=1084` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1958/english_certificate/english_certificate-66fdc650615f41838f1f7031cfbde954.pdf` | (missing) |

### candidate_no = SH20271053

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=519` `application_id=1085` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2276/english_certificate/english_certificate-6c94a98149914b64a9cd14b3861e4826.pdf` | (missing) |

### candidate_no = SH20271054

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=573` `application_id=1086` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2201/english_certificate/english_certificate-65d6fb1fca9e4507ad1ebd44f444a19b.pdf` | (missing) |

### candidate_no = SH20271055

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=884` `application_id=1087` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1682/english_certificate/english_certificate-dd6b0eddc89e46bf8085162f56c66104.pdf` | (missing) |

### candidate_no = SH20271056

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1440` `application_id=1088` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-837/english_certificate/english_certificate-7a803c6b3cad4edf8e30c8ca2baf48f4.pdf` | (missing) |

### candidate_no = SH20271057

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=926` `application_id=1089` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1597/english_certificate/english_certificate-4303c71076a04cb59f6119e1ac8d0d22.pdf` | (missing) |

### candidate_no = SH20271058

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=556` `application_id=1090` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2227/english_certificate/english_certificate-843a653e186c4d939e1e7ab111ff66a2.pdf` | (missing) |

### candidate_no = SH20271059

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1113` `application_id=1091` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1292/english_certificate/english_certificate-b21d0c8574b24c3e85f5de92e91c50f1.pdf` | (missing) |

### candidate_no = SH20271060

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1953` `application_id=1092` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-44/english_certificate/english_certificate-3208016af6594349a27414b49eb07c9a.pdf` | (missing) |

### candidate_no = SH20271061

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=971` `application_id=1093` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1517/english_certificate/english_certificate-5ca300da56444475a3a0699ef0ab0a61.pdf` | (missing) |

### candidate_no = SH20271062

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=646` `application_id=1094` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2074/english_certificate/english_certificate-b83409adaee04c0084770c218efe8b01.pdf` | (missing) |

### candidate_no = SH20271063

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=896` `application_id=1095` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1654/english_certificate/english_certificate-fda8147a85f0440ebcdfe43f8dad24f0.png` | (missing) |

### candidate_no = SH20271064

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=340` `application_id=1096` `exam_name=CET-6` `score_text=532` `certificate_attachment_url=/api/v1/portal/attachments/student-2589/english_certificate/english_certificate-ebe9995d83d64f8b8f9f972e4058660d.pdf` | (missing) |

### candidate_no = SH20271065

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=457` `application_id=1097` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2373/english_certificate/english_certificate-e750af64849d4068bb4e9003facb6aa5.pdf` | (missing) |

### candidate_no = SH20271066

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=354` `application_id=1098` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2568/english_certificate/english_certificate-dac4b32cfaaf46cc95f0f48615dcf2c9.pdf` | (missing) |

### candidate_no = SH20271067

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=761` `application_id=1099` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1874/english_certificate/english_certificate-29fdfc6e941b47dcb2f1af8d2b4bd483.pdf` | (missing) |

### candidate_no = SH20271068

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1156` `application_id=1100` `exam_name=CET-6` `score_text=565` `certificate_attachment_url=/api/v1/portal/attachments/student-1225/english_certificate/english_certificate-faaa6b2531f74c35984f3e17f43a7317.pdf` | (missing) |

### candidate_no = SH20271069

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1342` `application_id=1101` `exam_name=CET-6` `score_text=517` `certificate_attachment_url=/api/v1/portal/attachments/student-966/english_certificate/english_certificate-96808a16c8224cfb9b3ee643f0cfe7d1.pdf` | (missing) |

### candidate_no = SH20271070

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1370` `application_id=1102` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-923/english_certificate/english_certificate-99cf2723c505470f9d853f94edb294f3.pdf` | (missing) |

### candidate_no = SH20271071

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=539` `application_id=1103` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2247/english_certificate/english_certificate-6695a5bbf2654198ace7526640d3b0da.pdf` | (missing) |

### candidate_no = SH20271072

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1060` `application_id=1104` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1370/english_certificate/english_certificate-9ce09b50cb6c49b7816e38331c017508.pdf` | (missing) |

### candidate_no = SH20271073

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1831` `application_id=1105` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-213/english_certificate/english_certificate-7a5ee4ab23774ed6b8018d98d03aa0c6.pdf` | (missing) |

### candidate_no = SH20271074

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=908` `application_id=1106` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1630/english_certificate/english_certificate-d4cfa0a168034e5fb5f4fee9b9e51201.pdf` | (missing) |

### candidate_no = SH20271075

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=491` `application_id=1107` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2321/english_certificate/english_certificate-b00f707196db41b386968517b880bf1e.pdf` | (missing) |

### candidate_no = SH20271076

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=350` `application_id=1108` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2575/english_certificate/english_certificate-7a3a238163dd4c1dbde38a97d0cedc56.pdf` | (missing) |

### candidate_no = SH20271077

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=707` `application_id=1109` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1968/english_certificate/english_certificate-ec4f481006404fc2a6933bd3829143e1.pdf` | (missing) |

### candidate_no = SH20271078

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=337` `application_id=1110` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2592/english_certificate/english_certificate-1fde3c0373e343aea487cbb178f69193.pdf` | (missing) |

### candidate_no = SH20271079

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1786` `application_id=1111` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-292/english_certificate/english_certificate-93fb795275d74a88a1ec0227f9c88c91.pdf` | (missing) |

### candidate_no = SH20271080

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=605` `application_id=1112` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2145/english_certificate/english_certificate-ed627851f974485b865697a7631ede77.pdf` | (missing) |

### candidate_no = SH20271081

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=398` `application_id=1113` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2489/english_certificate/english_certificate-ae3fdf4daf9c48039cf0eadc98441cac.pdf` | (missing) |

### candidate_no = SH20271082

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1028` `application_id=1114` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1428/english_certificate/english_certificate-4a969f422c6f4634b5ff1c101bb42a5c.pdf` | (missing) |

### candidate_no = SH20271083

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=329` `application_id=1115` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2601/english_certificate/english_certificate-a7359917f62f4a2dba731fecf61e3b14.pdf` | (missing) |

### candidate_no = SH20271084

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=790` `application_id=1116` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1835/english_certificate/english_certificate-5547838bdb7b4afba7440654dddb87f4.pdf` | (missing) |

### candidate_no = SH20271085

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=804` `application_id=1117` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1819/english_certificate/english_certificate-14427c5b414f4ca59c8f274b9ca2b5ef.pdf` | (missing) |

### candidate_no = SH20271086

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=451` `application_id=1118` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2383/english_certificate/english_certificate-a7be36fd1c45449aac5ff3a2c60d55b8.pdf` | (missing) |

### candidate_no = SH20271087

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1551` `application_id=1119` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-667/english_certificate/english_certificate-41f6e2051c7d45a8b4a8a6be7279b375.pdf` | (missing) |

### candidate_no = SH20271088

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1956` `application_id=1120` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-41/english_certificate/english_certificate-5931e3cb38004323ab17fc046ac458fd.pdf` | (missing) |

### candidate_no = SH20271089

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1864` `application_id=1121` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-166/english_certificate/english_certificate-8bfb8aa96b48469ba1ab8cbf334f7826.pdf` | (missing) |

### candidate_no = SH20271090

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1027` `application_id=1122` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1430/english_certificate/english_certificate-9793aae3b4774ac195dd644b8ddf8f83.jpg` | (missing) |

### candidate_no = SH20271091

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1383` `application_id=1123` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-904/english_certificate/english_certificate-1b67fd88eb1c42acb7e20c56f53b40bd.pdf` | (missing) |

### candidate_no = SH20271092

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=950` `application_id=1124` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1554/english_certificate/english_certificate-06c229f464ba4cdd9bdc38117b156e28.pdf` | (missing) |

### candidate_no = SH20271093

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=807` `application_id=1125` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1816/english_certificate/english_certificate-6b8cb3e22d01499cbd5dcb63fc306304.pdf` | (missing) |

### candidate_no = SH20271094

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1053` `application_id=1126` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1385/english_certificate/english_certificate-b92dd2441b9247709cbed06f86b7f9d0.pdf` | (missing) |

### candidate_no = SH20271095

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=349` `application_id=1127` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2576/english_certificate/english_certificate-70073ef3e7a448089b065bce64f011f1.pdf` | (missing) |

### candidate_no = SH20271096

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1929` `application_id=1128` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-77/english_certificate/english_certificate-2f82525c50b44e5ebc6bb1f424d5351d.pdf` | (missing) |

### candidate_no = SH20271097

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1400` `application_id=1129` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-884/english_certificate/english_certificate-366949f050b74ea38041446cf4659bee.pdf` | (missing) |

### candidate_no = SH20271098

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=939` `application_id=1130` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1577/english_certificate/english_certificate-a692b698a75b43b8b89a3f07984afa8c.png` | (missing) |

### candidate_no = SH20271099

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=666` `application_id=1131` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2045/english_certificate/english_certificate-24602f78c280448ba2d5435c94023f81.pdf` | (missing) |

### candidate_no = SH20271100

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=415` `application_id=1132` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2454/english_certificate/english_certificate-a4f6f013ee9e46ff906f55da45a7193c.jpg` | (missing) |

### candidate_no = SH20271101

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1651` `application_id=1133` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-514/english_certificate/english_certificate-eab6db82b6b749ab802a36d35560365f.pdf` | (missing) |

### candidate_no = SH20271102

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1413` `application_id=1134` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-866/english_certificate/english_certificate-bf00af6a9ad045bf9c51f64b65013404.jpg` | (missing) |

### candidate_no = SH20271103

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=365` `application_id=1135` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2549/english_certificate/english_certificate-b113666dd2b54c029c74b446373fb9ee.pdf` | (missing) |

### candidate_no = SH20271104

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1785` `application_id=1136` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-293/english_certificate/english_certificate-7ee288d985854de2b21127995a973f64.pdf` | (missing) |

### candidate_no = SH20271105

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=598` `application_id=1137` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2151/english_certificate/english_certificate-84b3e744d3b74ab7b5938a062d39cc33.pdf` | (missing) |

### candidate_no = SH20271106

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=586` `application_id=1138` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2175/english_certificate/english_certificate-a33170d03b5a4eed822a11b6dcf9df2b.pdf` | (missing) |

### candidate_no = SH20271107

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1125` `application_id=1139` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1277/english_certificate/english_certificate-7c42c18b9dc04f8c9a476ed0784a6ec4.pdf` | (missing) |

### candidate_no = SH20271108

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=323` `application_id=1140` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2608/english_certificate/english_certificate-9e861f690a6e4ea8a323ecc4c515922c.pdf` | (missing) |

### candidate_no = SH20271109

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=446` `application_id=1141` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2389/english_certificate/english_certificate-be896bfb6e5849dda3bbfd2cb7178831.pdf` | (missing) |

### candidate_no = SH20271110

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=368` `application_id=1142` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2545/english_certificate/english_certificate-a0a80a053b6242e199f6d9a4c7bdb02b.pdf` | (missing) |

### candidate_no = SH20271111

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1843` `application_id=1143` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-199/english_certificate/english_certificate-6ce4ad443c694a0790f398d96f632d9c.png` | (missing) |

### candidate_no = SH20271112

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1836` `application_id=1144` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-207/english_certificate/english_certificate-8bce721c61d2477ba417f9cd42e0bbca.pdf` | (missing) |

### candidate_no = SH20271113

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=754` `application_id=1145` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1885/english_certificate/english_certificate-007e4132539c45f2a831f9da2be6ebb4.pdf` | (missing) |

### candidate_no = SH20271114

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=326` `application_id=1146` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2605/english_certificate/english_certificate-6058688c2ffd469ca4817d9b31103a2c.pdf` | (missing) |

### candidate_no = SH20271115

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1200` `application_id=1147` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1156/english_certificate/english_certificate-df96a1cc30844d03af7c83ce9cd50939.pdf` | (missing) |

### candidate_no = SH20271116

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=332` `application_id=1148` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2598/english_certificate/english_certificate-b54d9394acc24022bb31c4155b0568b1.pdf` | (missing) |

### candidate_no = SH20271117

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=396` `application_id=1149` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2494/english_certificate/english_certificate-fbd9648f5eb04c9ba9771644e8391a94.pdf` | (missing) |

### candidate_no = SH20271118

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1268` `application_id=1150` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1062/english_certificate/english_certificate-51a6ac059ae147c9a52a78b67424dfbc.pdf` | (missing) |

### candidate_no = SH20271119

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=312` `application_id=1151` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2622/english_certificate/english_certificate-8dd245c9230c4bcfb9cb32fa3f004aeb.pdf` | (missing) |

### candidate_no = SH20271120

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1581` `application_id=1152` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-620/english_certificate/english_certificate-164278b21f2d43cabf4b2d48acff8649.pdf` | (missing) |

### candidate_no = SH20271121

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1081` `application_id=1153` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1336/english_certificate/english_certificate-8cd1b7f2c5194f559f56cfd4d35b4940.pdf` | (missing) |

### candidate_no = SH20271122

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=311` `application_id=1154` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2624/english_certificate/english_certificate-717ae64c357c450faa6623f7cdc7939a.pdf` | (missing) |

### candidate_no = SH20271123

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=595` `application_id=1155` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2154/english_certificate/english_certificate-32e21e387b9644179b2d03a012beb75e.pdf` | (missing) |

### candidate_no = SH20271124

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=314` `application_id=1156` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2620/english_certificate/english_certificate-1781fe6a891e48a18e1bbe381badc919.jpg` | (missing) |

### candidate_no = SH20271125

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=668` `application_id=1157` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2042/english_certificate/english_certificate-9c4bfda0fef342718334128a41d1aad5.jpg` | (missing) |

### candidate_no = SH20271126

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=309` `application_id=1158` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2626/english_certificate/english_certificate-a0251e8dc6664b8fa75e9b0d75624043.pdf` | (missing) |

### candidate_no = SH20271127

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1695` `application_id=1159` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-451/english_certificate/english_certificate-cde1190767794cef9384d5071e6642bf.pdf` | (missing) |

### candidate_no = SH20271128

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=310` `application_id=1160` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2625/english_certificate/english_certificate-44e5b2ed63764f21a44d88f79ba44fab.pdf` | (missing) |

### candidate_no = SH20271129

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1139` `application_id=1161` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1255/english_certificate/english_certificate-06187ccf8c37415096c3a6db61c5737c.pdf` | (missing) |

### candidate_no = SH20271130

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1072` `application_id=1162` `exam_name=CET-6` `score_text=634` `certificate_attachment_url=/api/v1/portal/attachments/student-1350/english_certificate/english_certificate-a6d434a6a0d246a890d80f02b08e8297.pdf` | (missing) |

### candidate_no = SH20271131

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=389` `application_id=1163` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2505/english_certificate/english_certificate-464427fb6f0a407ba2097f2a78a09ac2.pdf` | (missing) |

### candidate_no = SH20271132

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1095` `application_id=1164` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1313/english_certificate/english_certificate-b054892384bc43c6a750d574270de87e.pdf` | (missing) |

### candidate_no = SH20271133

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1914` `application_id=1165` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-98/english_certificate/english_certificate-1f4d3d706b3447f1bb9cae5dd0f9b804.jpg` | (missing) |

### candidate_no = SH20271134

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=774` `application_id=1166` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1854/english_certificate/english_certificate-eebb2d4b2c50475db192cc9161bd6c5a.pdf` | (missing) |

### candidate_no = SH20271135

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=307` `application_id=1167` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2628/english_certificate/english_certificate-bb93420d49fd4aa1954b98b2c51f3710.pdf` | (missing) |

### candidate_no = SH20271136

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1622` `application_id=1168` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-555/english_certificate/english_certificate-db4e067461e74b8f8a6bbdf85c3f731e.pdf` | (missing) |

### candidate_no = SH20271137

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1925` `application_id=1169` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-83/english_certificate/english_certificate-0b5573046e9d4df3b8b132bb85582898.pdf` | (missing) |

### candidate_no = SH20271138

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=391` `application_id=1170` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2499/english_certificate/english_certificate-c2171e8b602c41a39ea3d67839d48fb0.pdf` | (missing) |

### candidate_no = SH20271139

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1803` `application_id=1171` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-261/english_certificate/english_certificate-c39e010598e84978b2cdb83d3348e35c.pdf` | (missing) |

### candidate_no = SH20271140

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1811` `application_id=1172` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-250/english_certificate/english_certificate-3c768988a3214688a3e5d7999181741c.pdf` | (missing) |

### candidate_no = SH20271141

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=394` `application_id=1173` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2496/english_certificate/english_certificate-d43f427e0a2b43b9a2a79550066cd332.pdf` | (missing) |

### candidate_no = SH20271142

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=479` `application_id=1174` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2342/english_certificate/english_certificate-8386b188bcbe4ed2a14a7e5fe1300f7d.pdf` | (missing) |

### candidate_no = SH20271143

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=516` `application_id=1175` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2280/english_certificate/english_certificate-9aa45cfcc10840fcada54b6cd1e5e1c3.pdf` | (missing) |

### candidate_no = SH20271144

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1840` `application_id=1176` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-202/english_certificate/english_certificate-6f13594a0eb74b8d8e45f087b4accbbc.png` | (missing) |

### candidate_no = SH20271145

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=622` `application_id=1177` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2111/english_certificate/english_certificate-0d751546926a4cc0b7598bc122d86cc4.pdf` | (missing) |

### candidate_no = SH20271146

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1605` `application_id=1178` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-582/english_certificate/english_certificate-c8ccf219f4bf4ab29602bea1cf3fceaa.jpg` | (missing) |

### candidate_no = SH20271147

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=744` `application_id=1179` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1903/english_certificate/english_certificate-3ed536d54dd046158e120cf84a79fbbe.jpeg` | (missing) |

### candidate_no = SH20271148

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1190` `application_id=1180` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1168/english_certificate/english_certificate-de9acfffbc7042d3bde2933828061867.jpg` | (missing) |

### candidate_no = SH20271149

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=295` `application_id=1181` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2644/english_certificate/english_certificate-e25bdcd041c440d791b82b4c3e4c78c7.pdf` | (missing) |

### candidate_no = SH20271150

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=616` `application_id=1182` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2129/english_certificate/english_certificate-eed635f1a0e948f0b818124f7c0d3aef.pdf` | (missing) |

### candidate_no = SH20271151

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=290` `application_id=1183` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2654/english_certificate/english_certificate-def4ee74befb41ed9ab3490f5d10924d.pdf` | (missing) |

### candidate_no = SH20271152

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1138` `application_id=1184` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1257/english_certificate/english_certificate-eb80c9d6fa854e92b1b4db133ca56f45.jpg` | (missing) |

### candidate_no = SH20271153

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1196` `application_id=1185` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1162/english_certificate/english_certificate-34d4a3141aec4fef99d80385269f0950.pdf` | (missing) |

### candidate_no = SH20271154

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1745` `application_id=1186` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-374/english_certificate/english_certificate-00731ff67a604e3791901702570744f1.pdf` | (missing) |

### candidate_no = SH20271155

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=345` `application_id=1187` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2580/english_certificate/english_certificate-72d2684fca0c4ed6b25c82dcc5df8da4.pdf` | (missing) |

### candidate_no = SH20271156

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1349` `application_id=1188` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-955/english_certificate/english_certificate-5c33d4713d4d4e1d89fcb355c72d60e5.pdf` | (missing) |

### candidate_no = SH20271157

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=538` `application_id=1189` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2249/english_certificate/english_certificate-7f4a136719e9452da90151a4d575014d.pdf` | (missing) |

### candidate_no = SH20271158

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1662` `application_id=1190` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-499/english_certificate/english_certificate-4661724d092f4cb19e4ee10f04d12f56.pdf` | (missing) |

### candidate_no = SH20271159

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1469` `application_id=1191` `exam_name=CET-6` `score_text=518` `certificate_attachment_url=/api/v1/portal/attachments/student-791/english_certificate/english_certificate-6442e0df389f4230b2baef1c5834af6b.pdf` | (missing) |

### candidate_no = SH20271160

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=305` `application_id=1192` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2633/english_certificate/english_certificate-377e1526d9bc43a3b345a97f1dfc33f7.pdf` | (missing) |

### candidate_no = SH20271161

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=424` `application_id=1193` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2429/english_certificate/english_certificate-9758de9097814222879473df4d28b879.jpg` | (missing) |

### candidate_no = SH20271162

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=362` `application_id=1194` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2557/english_certificate/english_certificate-354a934a208c49d3a09caeb878be8ce6.pdf` | (missing) |

### candidate_no = SH20271163

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1850` `application_id=1195` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-186/english_certificate/english_certificate-235983b333a349f4b47292ec17e1c4b5.pdf` | (missing) |

### candidate_no = SH20271164

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=339` `application_id=1196` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2590/english_certificate/english_certificate-9c8913b2b6514974a90d5ee82da12bed.pdf` | (missing) |

### candidate_no = SH20271165

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=580` `application_id=1197` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2184/english_certificate/english_certificate-81bb9ef4a69b40ec9174ae01d70a482f.pdf` | (missing) |

### candidate_no = SH20271166

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=437` `application_id=1198` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2401/english_certificate/english_certificate-7c02d182487a49df84cd7b6efb891d3f.pdf` | (missing) |

### candidate_no = SH20271167

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=283` `application_id=1199` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2664/english_certificate/english_certificate-459e60b3b84f4f9eb83638a13eeb8574.pdf` | (missing) |

### candidate_no = SH20271168

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1026` `application_id=1200` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1431/english_certificate/english_certificate-5b77b00f57d84782b0ab84feca6f04da.pdf` | (missing) |

### candidate_no = SH20271169

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=289` `application_id=1201` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2656/english_certificate/english_certificate-bf8f3fe4624d4157a70555c9162c9076.pdf` | (missing) |

### candidate_no = SH20271170

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=655` `application_id=1202` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2062/english_certificate/english_certificate-bb60e8d97eb34fe7a1658a2e1b241653.pdf` | (missing) |

### candidate_no = SH20271171

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=280` `application_id=1203` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2667/english_certificate/english_certificate-b24566159f164a82ab86e6d7aefefd07.pdf` | (missing) |

### candidate_no = SH20271172

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1769` `application_id=1204` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-327/english_certificate/english_certificate-e1c7edf299754608881a4d739cc93d1e.pdf` | (missing) |

### candidate_no = SH20271173

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=294` `application_id=1205` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2648/english_certificate/english_certificate-495389e912a64a60be9981c9e32b5737.pdf` | (missing) |

### candidate_no = SH20271174

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1044` `application_id=1206` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1396/english_certificate/english_certificate-4c050f4ea7b44216ba88eb9f299ffa7d.pdf` | (missing) |

### candidate_no = SH20271175

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=907` `application_id=1207` `exam_name=CET-6` `score_text=534` `certificate_attachment_url=/api/v1/portal/attachments/student-1632/english_certificate/english_certificate-78bcfcec8e164e448980d9451f60c414.pdf` | (missing) |

### candidate_no = SH20271176

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=279` `application_id=1208` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2668/english_certificate/english_certificate-2ccdde1546804c99889149d7424721ae.pdf` | (missing) |

### candidate_no = SH20271177

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1731` `application_id=1209` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-396/english_certificate/english_certificate-b4afa4a798e5430dae50b82856cf5ef4.pdf` | (missing) |

### candidate_no = SH20271178

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=286` `application_id=1210` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2660/english_certificate/english_certificate-7b0d1355c7104b9294a17e53f71941e0.pdf` | (missing) |

### candidate_no = SH20271179

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=755` `application_id=1211` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1883/english_certificate/english_certificate-ff26d43eeaa84faeb032153e6f2d2614.pdf` | (missing) |

### candidate_no = SH20271180

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=639` `application_id=1212` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2083/english_certificate/english_certificate-ed6bf176ab2d487bbb47fb46d12c89dd.pdf` | (missing) |

### candidate_no = SH20271181

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=530` `application_id=1213` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2261/english_certificate/english_certificate-7d4188ddd28b4a55bd20fac2fa3063c9.pdf` | (missing) |

### candidate_no = SH20271182

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=285` `application_id=1214` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2662/english_certificate/english_certificate-8c952c05ad934ce2885ed1f421cc61c1.pdf` | (missing) |

### candidate_no = SH20271183

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=270` `application_id=1215` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2679/english_certificate/english_certificate-2ebd6df1ff5e4055874e974045a7d7cd.jpg` | (missing) |

### candidate_no = SH20271184

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=407` `application_id=1216` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2470/english_certificate/english_certificate-6a7f011d64f4499580703f5c4355434b.pdf` | (missing) |

### candidate_no = SH20271185

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=763` `application_id=1217` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1871/english_certificate/english_certificate-7f687c1b498449c6b1c7fefaea407f8d.pdf` | (missing) |

### candidate_no = SH20271186

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=624` `application_id=1218` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2107/english_certificate/english_certificate-95d3a7291aa74961934cc35983a30583.pdf` | (missing) |

### candidate_no = SH20271187

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=775` `application_id=1219` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1853/english_certificate/english_certificate-fce8aa4204484846b4fb59f428b73556.pdf` | (missing) |

### candidate_no = SH20271188

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=335` `application_id=1220` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2595/english_certificate/english_certificate-5841afa406f44981950e687a2fd6db98.pdf` | (missing) |

### candidate_no = SH20271189

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=422` `application_id=1221` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2435/english_certificate/english_certificate-8b58c478095e419f8ac904c7e1faa4fd.png` | (missing) |

### candidate_no = SH20271190

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=787` `application_id=1222` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1838/english_certificate/english_certificate-be1adb6dc4ce4231a43ca423f81b6081.pdf` | (missing) |

### candidate_no = SH20271191

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=264` `application_id=1223` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2687/english_certificate/english_certificate-a3894c326e3e42ebbcaf6d0b00c759a4.pdf` | (missing) |

### candidate_no = SH20271192

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=678` `application_id=1224` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2025/english_certificate/english_certificate-fc04fbc1ccc94b2daaeb2c605b5cc474.jpg` | (missing) |

### candidate_no = SH20271193

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=377` `application_id=1225` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2534/english_certificate/english_certificate-4ad4372f6f36450abfc8fc3ccc85eb03.png` | (missing) |

### candidate_no = SH20271194

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1035` `application_id=1226` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1416/english_certificate/english_certificate-cd8dfdad6ea443b790fd9394d84819b3.pdf` | (missing) |

### candidate_no = SH20271195

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=282` `application_id=1227` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2665/english_certificate/english_certificate-cf68ea5298d3435e9354df1a4526da5a.pdf` | (missing) |

### candidate_no = SH20271196

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=261` `application_id=1228` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2690/english_certificate/english_certificate-663fbc5ddfd74f189c52bf58a4dc905f.pdf` | (missing) |

### candidate_no = SH20271197

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=506` `application_id=1229` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2296/english_certificate/english_certificate-b08996a18ba34c47a62388e5aed1b933.pdf` | (missing) |

### candidate_no = SH20271198

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1214` `application_id=1230` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1132/english_certificate/english_certificate-22012f53957c4500828ecd55d0d7f754.pdf` | (missing) |

### candidate_no = SH20271199

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=400` `application_id=1231` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2486/english_certificate/english_certificate-660872adb46247ecaab7247475f88dce.pdf` | (missing) |

### candidate_no = SH20271200

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=560` `application_id=1232` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2223/english_certificate/english_certificate-bdd2159db0894e7fafe3420202691555.jpg` | (missing) |

### candidate_no = SH20271201

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=677` `application_id=1233` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2028/english_certificate/english_certificate-273097987e834cb9a08d38d23555ce76.pdf` | (missing) |

### candidate_no = SH20271202

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1689` `application_id=1234` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-458/english_certificate/english_certificate-794f6baf8a8d47fda4426f618f983da5.pdf` | (missing) |

### candidate_no = SH20271203

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=999` `application_id=1235` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1472/english_certificate/english_certificate-acc8c6020d4f478bbc09869f6563e5ee.pdf` | (missing) |

### candidate_no = SH20271204

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1570` `application_id=1236` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-635/english_certificate/english_certificate-d6ce9f05d1dc4d76b7ba1dcf9cde73b0.pdf` | (missing) |

### candidate_no = SH20271205

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1152` `application_id=1237` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1236/english_certificate/english_certificate-5f64a18b2ee043afbc7f3bfd3f519731.pdf` | (missing) |

### candidate_no = SH20271206

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=293` `application_id=1238` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2650/english_certificate/english_certificate-c041b2c257864e6b83e17f81a1497b44.pdf` | (missing) |

### candidate_no = SH20271207

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=835` `application_id=1239` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1765/english_certificate/english_certificate-4162488561ec4a66bb433006b11bc3af.pdf` | (missing) |

### candidate_no = SH20271208

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=547` `application_id=1240` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2238/english_certificate/english_certificate-a8c78d27e7514b1eb4fc0554aca3d6a6.pdf` | (missing) |

### candidate_no = SH20271209

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=348` `application_id=1241` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2577/english_certificate/english_certificate-e9be40c46d694492860d3007c1a37198.pdf` | (missing) |

### candidate_no = SH20271210

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=669` `application_id=1242` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2040/english_certificate/english_certificate-3c4c07afd1714faaa8c1c53b11bda148.pdf` | (missing) |

### candidate_no = SH20271211

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=870` `application_id=1243` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1705/english_certificate/english_certificate-c8c870956fb541e9bfb590726a71dc06.jpg` | (missing) |

### candidate_no = SH20271212

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=278` `application_id=1244` `exam_name=CET-6` `score_text=597` `certificate_attachment_url=/api/v1/portal/attachments/student-2669/english_certificate/english_certificate-33b3a5897ea04ab1b1392b1d563e2129.jpg` | (missing) |

### candidate_no = SH20271213

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=517` `application_id=1245` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2279/english_certificate/english_certificate-0a921b50300d419d8625e785f4e6d0b9.pdf` | (missing) |

### candidate_no = SH20271214

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=260` `application_id=1246` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2692/english_certificate/english_certificate-e5f738145bb14c1aa6d68d6717458660.pdf` | (missing) |

### candidate_no = SH20271215

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=265` `application_id=1247` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2686/english_certificate/english_certificate-2efbcf5e34254b89a939da610821fc94.pdf` | (missing) |

### candidate_no = SH20271216

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1140` `application_id=1248` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1254/english_certificate/english_certificate-322386f0569c4f11bb04c0d781ba5b3d.pdf` | (missing) |

### candidate_no = SH20271217

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1835` `application_id=1249` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-208/english_certificate/english_certificate-332de3ff59824938ac1b8b39e6fe015a.pdf` | (missing) |

### candidate_no = SH20271218

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1620` `application_id=1250` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-558/english_certificate/english_certificate-4aa756c14a50489aad49b591f489197b.pdf` | (missing) |

### candidate_no = SH20271219

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1488` `application_id=1251` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-763/english_certificate/english_certificate-937118bed0754ca6a7cf730eca75b758.pdf` | (missing) |

### candidate_no = SH20271220

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1499` `application_id=1252` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-749/english_certificate/english_certificate-9d6f54e5e4894ea2879d7001cabeef71.pdf` | (missing) |

### candidate_no = SH20271221

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=271` `application_id=1253` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2677/english_certificate/english_certificate-df387d911d3849ca97236f1c9f6de9a7.pdf` | (missing) |

### candidate_no = SH20271222

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=871` `application_id=1254` `exam_name=CET-6` `score_text=537` `certificate_attachment_url=/api/v1/portal/attachments/student-1703/english_certificate/english_certificate-0843c5381d504320b8953b675dce8ddb.pdf` | (missing) |
| 第 2 行 | `id=872` `application_id=1254` `exam_name=IELTS` `score_text=6.0` `certificate_attachment_url=/api/v1/portal/attachments/student-1703/english_certificate/english_certificate-5f3751f35ebd45b499cc0d3e45fa2d82.pdf` | (missing) |

### candidate_no = SH20271223

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1455` `application_id=1255` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-815/english_certificate/english_certificate-39f792956f91494c8a4470d5a2c06d52.pdf` | (missing) |

### candidate_no = SH20271224

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1550` `application_id=1256` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-668/english_certificate/english_certificate-0ea92166f04c498cb5e20ac994224a54.pdf` | (missing) |

### candidate_no = SH20271225

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=498` `application_id=1257` `exam_name=CET-6` `score_text=573` `certificate_attachment_url=/api/v1/portal/attachments/student-2308/english_certificate/english_certificate-efed42f2380042188aa74f97fdd9d649.pdf` | (missing) |

### candidate_no = SH20271226

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=990` `application_id=1258` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1490/english_certificate/english_certificate-e83d724b372b4b28a24d120fd06dd114.pdf` | (missing) |

### candidate_no = SH20271227

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=496` `application_id=1259` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2311/english_certificate/english_certificate-8b9601463c224546acdaf15a8dc373b6.jpg` | (missing) |

### candidate_no = SH20271228

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1341` `application_id=1260` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-967/english_certificate/english_certificate-3dc934ba02e948f084f0e62ef843064b.pdf` | (missing) |

### candidate_no = SH20271229

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=251` `application_id=1261` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2706/english_certificate/english_certificate-9492b9917eef420facbdf57f66a0bca4.pdf` | (missing) |

### candidate_no = SH20271230

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=869` `application_id=1262` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1707/english_certificate/english_certificate-ff37dc84f0cc4174b8e92f611302e7f9.pdf` | (missing) |

### candidate_no = SH20271231

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=315` `application_id=1263` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2619/english_certificate/english_certificate-feb9d7d0c7a84784856aa5cb0faef59e.pdf` | (missing) |

### candidate_no = SH20271232

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1614` `application_id=1264` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-569/english_certificate/english_certificate-a1835ea56f4e429d812d4d70c68e8cd6.pdf` | (missing) |

### candidate_no = SH20271233

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=252` `application_id=1265` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2705/english_certificate/english_certificate-cbcfa620f37345b98a9ac4f264e3d560.pdf` | (missing) |

### candidate_no = SH20271234

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=334` `application_id=1266` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2596/english_certificate/english_certificate-d1016d1f123147bbbf32bb3e4e5d8cf1.pdf` | (missing) |

### candidate_no = SH20271235

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=253` `application_id=1267` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2704/english_certificate/english_certificate-f8c17ccdb7394e3195f1a434fd1d65e9.png` | (missing) |

### candidate_no = SH20271236

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=816` `application_id=1268` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1804/english_certificate/english_certificate-c799fece827b4e8e8c9c570dcc6ac3eb.pdf` | (missing) |

### candidate_no = SH20271237

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=243` `application_id=1269` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2716/english_certificate/english_certificate-6f7078b9be5745fc80b4647e274480b3.pdf` | (missing) |

### candidate_no = SH20271238

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=631` `application_id=1270` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2097/english_certificate/english_certificate-2e215c541a6a43288e6eb685df4c4c27.pdf` | (missing) |

### candidate_no = SH20271239

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1615` `application_id=1271` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-568/english_certificate/english_certificate-e9cb8634c5ba411783b0983b322f13e1.pdf` | (missing) |

### candidate_no = SH20271240

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=336` `application_id=1272` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2593/english_certificate/english_certificate-a61e61fea7724f01929e62fe68653776.pdf` | (missing) |

### candidate_no = SH20271241

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1016` `application_id=1273` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1448/english_certificate/english_certificate-3cabf89eb1df426cb17392032ac22146.pdf` | (missing) |

### candidate_no = SH20271242

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1015` `application_id=1274` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1449/english_certificate/english_certificate-f9e5a00808ba4ea8b59ba9da25988420.pdf` | (missing) |

### candidate_no = SH20271243

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1373` `application_id=1275` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-918/english_certificate/english_certificate-17b9f40eb6c4461996fcdef247cb98de.pdf` | (missing) |

### candidate_no = SH20271244

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=241` `application_id=1276` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2718/english_certificate/english_certificate-0630116268e54ffd83c7e6a3d62bab3b.pdf` | (missing) |

### candidate_no = SH20271245

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=239` `application_id=1277` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2722/english_certificate/english_certificate-319697cf7b624e81b6e364bfcec21345.png` | (missing) |

### candidate_no = SH20271246

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=244` `application_id=1278` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2715/english_certificate/english_certificate-44366cda3be64c2ca39e8a396d4b2705.pdf` | (missing) |

### candidate_no = SH20271247

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=277` `application_id=1279` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2670/english_certificate/english_certificate-251f09853c3340ea8d1e26d5b493898c.pdf` | (missing) |

### candidate_no = SH20271248

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=740` `application_id=1280` `exam_name=CET-6` `score_text=583` `certificate_attachment_url=/api/v1/portal/attachments/student-1911/english_certificate/english_certificate-190e69074b984d68841d07ac7b1bfc08.pdf` | (missing) |

### candidate_no = SH20271249

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=237` `application_id=1281` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2724/english_certificate/english_certificate-a719929c7de04938872e67a122c7da73.pdf` | (missing) |

### candidate_no = SH20271250

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=698` `application_id=1282` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1981/english_certificate/english_certificate-6e6c0e228ccd4ad0935a2bf9905fb38a.pdf` | (missing) |

### candidate_no = SH20271251

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1345` `application_id=1283` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-963/english_certificate/english_certificate-8d08f6d5af76499b872fe462b10c5112.pdf` | (missing) |

### candidate_no = SH20271252

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1222` `application_id=1284` `exam_name=CET-6` `score_text=582` `certificate_attachment_url=/api/v1/portal/attachments/student-1122/english_certificate/english_certificate-33b4cdfbf4fd4825a0d4e013cb2223c9.pdf` | (missing) |
| 第 2 行 | `id=1223` `application_id=1284` `exam_name=其他` `score_text=646` `certificate_attachment_url=/api/v1/portal/attachments/student-1122/english_certificate/english_certificate-f5598e1c21ee4c3fb4f5b0ba7ade08f3.pdf` | (missing) |

### candidate_no = SH20271253

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=327` `application_id=1285` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2604/english_certificate/english_certificate-9bd3e2fbf3f84a589a5cbdcee8a89e78.pdf` | (missing) |

### candidate_no = SH20271254

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=281` `application_id=1286` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2666/english_certificate/english_certificate-455b7a4696054b88ac10e587273df1cb.pdf` | (missing) |

### candidate_no = SH20271255

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1495` `application_id=1287` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-753/english_certificate/english_certificate-6bf36ccc1b8e4d468886d74b4c9ba634.jpg` | (missing) |

### candidate_no = SH20271256

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1230` `application_id=1288` `exam_name=CET-6` `score_text=494` `certificate_attachment_url=/api/v1/portal/attachments/student-1113/english_certificate/english_certificate-8e0388de1e934defabda7ef09f6a7993.pdf` | (missing) |

### candidate_no = SH20271257

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1880` `application_id=1289` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-144/english_certificate/english_certificate-378d60a0e94e4a60853e98dc10af3462.pdf` | (missing) |

### candidate_no = SH20271258

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=328` `application_id=1290` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2603/english_certificate/english_certificate-39fbb36cf7484964be777d2df26dac34.pdf` | (missing) |

### candidate_no = SH20271259

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=772` `application_id=1291` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1858/english_certificate/english_certificate-f307cc9dc5a2423a8e979b04035334b6.pdf` | (missing) |

### candidate_no = SH20271260

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=258` `application_id=1292` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2695/english_certificate/english_certificate-bccdb4f65b66456bb016084e0c7bf240.pdf` | (missing) |

### candidate_no = SH20271261

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1025` `application_id=1293` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1433/english_certificate/english_certificate-fa52a00f747f4477a3f000d26e124617.pdf` | (missing) |

### candidate_no = SH20271262

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1096` `application_id=1294` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1312/english_certificate/english_certificate-04fdfe7262ff44cab060e0ac66e1f7ee.pdf` | (missing) |

### candidate_no = SH20271263

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1721` `application_id=1295` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-411/english_certificate/english_certificate-3ee894394d18409f89c1da53e2a4413c.pdf` | (missing) |

### candidate_no = SH20271264

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=254` `application_id=1296` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2702/english_certificate/english_certificate-5c3dcad8b8724c65af194f8c5873c33a.pdf` | (missing) |

### candidate_no = SH20271265

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1253` `application_id=1297` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1078/english_certificate/english_certificate-de727a9198ad4d0eb254b536b58ba885.pdf` | (missing) |

### candidate_no = SH20271266

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=222` `application_id=1298` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2741/english_certificate/english_certificate-2238e097cf9143cbb6ca249b4a0ff7ca.pdf` | (missing) |

### candidate_no = SH20271267

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=236` `application_id=1299` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2726/english_certificate/english_certificate-9196ac11165e45d3b79a5a129470af1a.pdf` | (missing) |

### candidate_no = SH20271268

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1399` `application_id=1300` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-885/english_certificate/english_certificate-06f45e85c77c446e8759991578a1f275.pdf` | (missing) |

### candidate_no = SH20271269

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=224` `application_id=1301` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2739/english_certificate/english_certificate-91a4aa2605c241cba3acb56722c84142.jpg` | (missing) |

### candidate_no = SH20271270

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=619` `application_id=1302` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2119/english_certificate/english_certificate-9ec207fbe02946b69334c9dfdeefee89.pdf` | (missing) |

### candidate_no = SH20271271

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=226` `application_id=1303` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2737/english_certificate/english_certificate-9cd3b035382d4fe2bbbfb56a6180f1f8.pdf` | (missing) |

### candidate_no = SH20271272

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1599` `application_id=1304` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-594/english_certificate/english_certificate-dff72ddf0b2a4cb0824fe2b6097e88ed.pdf` | (missing) |

### candidate_no = SH20271273

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1042` `application_id=1305` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1398/english_certificate/english_certificate-7cc5d21158b64e6aa22e0f3c307aae90.pdf` | (missing) |

### candidate_no = SH20271274

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=683` `application_id=1306` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2019/english_certificate/english_certificate-44e9916dcd4946f49a75642c0ed1795b.pdf` | (missing) |

### candidate_no = SH20271275

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=717` `application_id=1307` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1950/english_certificate/english_certificate-ad1eb546f8ae479e8a9d91e9c1505f12.pdf` | (missing) |

### candidate_no = SH20271276

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=421` `application_id=1308` `exam_name=CET-6` `score_text=471` `certificate_attachment_url=/api/v1/portal/attachments/student-2437/english_certificate/english_certificate-32458fd902f342ef85aa7d41391b6f9c.pdf` | (missing) |

### candidate_no = SH20271277

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=674` `application_id=1309` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2031/english_certificate/english_certificate-f6ea496b67c64950b2178ebb51d0c0c5.pdf` | (missing) |

### candidate_no = SH20271278

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=322` `application_id=1310` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2609/english_certificate/english_certificate-7fcd958947b84f4eaeb80a63f1af3cfc.pdf` | (missing) |

### candidate_no = SH20271279

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=463` `application_id=1311` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2363/english_certificate/english_certificate-8d08ae1766c14b0297e05acdcaf46c9b.pdf` | (missing) |

### candidate_no = SH20271280

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1068` `application_id=1312` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1356/english_certificate/english_certificate-5db4935cd8d040e2b35159fd66517c9a.jpg` | (missing) |

### candidate_no = SH20271281

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1166` `application_id=1313` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1211/english_certificate/english_certificate-99aa4094423c4d85ba747f590f446214.pdf` | (missing) |

### candidate_no = SH20271282

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=510` `application_id=1314` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2287/english_certificate/english_certificate-5d187f4f908745ceb85d992f0e118781.pdf` | (missing) |

### candidate_no = SH20271283

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=710` `application_id=1315` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1964/english_certificate/english_certificate-029ed6e03697447a8c3fa8ecdd49d073.pdf` | (missing) |

### candidate_no = SH20271284

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=589` `application_id=1316` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2170/english_certificate/english_certificate-99de999d0c114d9194f9637ae415ae35.pdf` | (missing) |

### candidate_no = SH20271285

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=313` `application_id=1317` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2621/english_certificate/english_certificate-23f76d559ce745bc9b3b451361069eb4.png` | (missing) |

### candidate_no = SH20271286

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=760` `application_id=1318` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1875/english_certificate/english_certificate-b358ea13506e4db5b0be77a37574298e.pdf` | (missing) |

### candidate_no = SH20271287

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1479` `application_id=1319` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-775/english_certificate/english_certificate-db12ca525033459eae2182368d2fec8a.pdf` | (missing) |

### candidate_no = SH20271288

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1385` `application_id=1320` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-900/english_certificate/english_certificate-9c2606adba0d438fa34c0f43da93436b.pdf` | (missing) |

### candidate_no = SH20271289

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=848` `application_id=1321` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1740/english_certificate/english_certificate-a7c374cf427c42079e5aef23c0822afb.pdf` | (missing) |

### candidate_no = SH20271290

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=957` `application_id=1322` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1540/english_certificate/english_certificate-101554ed17284d42a09b1b656da77053.pdf` | (missing) |

### candidate_no = SH20271291

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1418` `application_id=1323` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-861/english_certificate/english_certificate-099c818b600749dba271a69ae47cbe34.pdf` | (missing) |

### candidate_no = SH20271292

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=227` `application_id=1324` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2736/english_certificate/english_certificate-8ed326c1a1a343b0b43b62f94f6f67a0.pdf` | (missing) |

### candidate_no = SH20271293

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=199` `application_id=1325` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2775/english_certificate/english_certificate-da0cc5c0bf0a4e7fb0f13338bf9f0039.pdf` | (missing) |

### candidate_no = SH20271294

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=219` `application_id=1326` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2748/english_certificate/english_certificate-3c48c8e2c27b4c30beb0abbd83c7c35a.pdf` | (missing) |

### candidate_no = SH20271295

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1822` `application_id=1327` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-227/english_certificate/english_certificate-b23244c0e0874abeaf9b52b9157cc4d9.pdf` | (missing) |

### candidate_no = SH20271296

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=300` `application_id=1328` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2638/english_certificate/english_certificate-995dfbcae5454be7a2bdeaf3c7c04f73.pdf` | (missing) |

### candidate_no = SH20271297

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=211` `application_id=1329` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2759/english_certificate/english_certificate-481fac81367c4837b35b614a1eb1b958.pdf` | (missing) |

### candidate_no = SH20271298

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=215` `application_id=1330` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2754/english_certificate/english_certificate-6de2d5b426994c7d91d99ef29ef95a60.png` | (missing) |

### candidate_no = SH20271299

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=487` `application_id=1331` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2325/english_certificate/english_certificate-1fccce47cb494d6c81a754a2704ccbfa.pdf` | (missing) |

### candidate_no = SH20271300

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1119` `application_id=1332` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1283/english_certificate/english_certificate-e8f889c34bae40f1ade63f8bb1445b49.pdf` | (missing) |

### candidate_no = SH20271301

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=194` `application_id=1333` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2782/english_certificate/english_certificate-449b21554f114476a32fddba6ca9e17c.pdf` | (missing) |

### candidate_no = SH20271302

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=863` `application_id=1334` `exam_name=CET-6` `score_text=501` `certificate_attachment_url=/api/v1/portal/attachments/student-1716/english_certificate/english_certificate-a0bca2f115d8424cbce7166669d65ebb.pdf` | (missing) |

### candidate_no = SH20271303

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=981` `application_id=1335` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1503/english_certificate/english_certificate-2ec124a6a0bd4bdaba22c0e00ef73663.pdf` | (missing) |

### candidate_no = SH20271304

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=195` `application_id=1336` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2780/english_certificate/english_certificate-2738e3bef34d4fa790affa013064fed9.pdf` | (missing) |

### candidate_no = SH20271305

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1208` `application_id=1337` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1140/english_certificate/english_certificate-bb02854f69ab480891bdc6188005737d.pdf` | (missing) |

### candidate_no = SH20271306

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=202` `application_id=1338` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2772/english_certificate/english_certificate-01956b4a9b5742c0838e93a4407b7fcf.pdf` | (missing) |

### candidate_no = SH20271307

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1408` `application_id=1339` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-871/english_certificate/english_certificate-4bb37f3f0fa04c2d82bbcb463c5f04bf.pdf` | (missing) |

### candidate_no = SH20271308

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=858` `application_id=1340` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1723/english_certificate/english_certificate-4cecb9f1dfc54da48152ab3e845717ea.pdf` | (missing) |

### candidate_no = SH20271309

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1908` `application_id=1341` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-103/english_certificate/english_certificate-d85723db951148f4a4efa8f991525528.pdf` | (missing) |

### candidate_no = SH20271310

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=555` `application_id=1342` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2228/english_certificate/english_certificate-ceaebe79c0194ef2972da83b0876eac2.pdf` | (missing) |

### candidate_no = SH20271311

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1967` `application_id=1343` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-27/english_certificate/english_certificate-428c4380c7284c4485a7a39825c5dbd0.pdf` | (missing) |

### candidate_no = SH20271312

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=892` `application_id=1344` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1661/english_certificate/english_certificate-4e3f7a24846c4ba39c8fad3f11078393.pdf` | (missing) |

### candidate_no = SH20271313

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=485` `application_id=1345` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2327/english_certificate/english_certificate-7d546d27efc74f4b9ff59c5dec808539.pdf` | (missing) |

### candidate_no = SH20271314

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=191` `application_id=1346` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2787/english_certificate/english_certificate-60dc3cd06c7e429cb19d02f7945d90e1.pdf` | (missing) |

### candidate_no = SH20271315

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=493` `application_id=1347` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2318/english_certificate/english_certificate-1c17788a9d7e46cda5fafd644dde4703.pdf` | (missing) |

### candidate_no = SH20271316

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=387` `application_id=1348` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2509/english_certificate/english_certificate-e8356423eb0c44bcbb00fb9115fe5ac1.pdf` | (missing) |

### candidate_no = SH20271317

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1039` `application_id=1349` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1404/english_certificate/english_certificate-c66a2a1c9d4d4ee093fcfd9e20e81541.pdf` | (missing) |

### candidate_no = SH20271318

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=193` `application_id=1350` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2783/english_certificate/english_certificate-447baa69a3cf409d8d0f75db5d34782a.pdf` | (missing) |

### candidate_no = SH20271319

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=419` `application_id=1351` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2439/english_certificate/english_certificate-9494c4158f514ffc9a0600005ef40c6e.pdf` | (missing) |

### candidate_no = SH20271320

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=382` `application_id=1352` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2522/english_certificate/english_certificate-2d8bea8c421b4daeab9421aa05c63f54.jpg` | (missing) |

### candidate_no = SH20271321

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1528` `application_id=1353` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-702/english_certificate/english_certificate-7ae7bd600d5f4fb7880871298a28e6c1.png` | (missing) |

### candidate_no = SH20271322

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=276` `application_id=1354` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2672/english_certificate/english_certificate-fd58efae874c42888dde91c7389da1b4.pdf` | (missing) |

### candidate_no = SH20271323

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=918` `application_id=1355` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1608/english_certificate/english_certificate-817db910971147758949f56f6d06c1ce.pdf` | (missing) |

### candidate_no = SH20271324

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=410` `application_id=1356` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2464/english_certificate/english_certificate-0655b2c8491d4563bf7c4add1f2e0a0b.pdf` | (missing) |

### candidate_no = SH20271325

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1252` `application_id=1357` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1079/english_certificate/english_certificate-95463683df6b49d29c9a128ace76f41c.pdf` | (missing) |

### candidate_no = SH20271326

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1671` `application_id=1358` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-486/english_certificate/english_certificate-3054c7201693432aa3bb9856bdcbd427.pdf` | (missing) |

### candidate_no = SH20271327

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=189` `application_id=1359` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2789/english_certificate/english_certificate-427167e840bf46c5a359635902cbe4ea.pdf` | (missing) |

### candidate_no = SH20271328

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=965` `application_id=1360` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1528/english_certificate/english_certificate-0b68d1cd84db42a5acd67720df5aa478.jpg` | (missing) |

### candidate_no = SH20271329

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=376` `application_id=1361` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2535/english_certificate/english_certificate-01af09d0473e4b8fa811b597e9a7a05f.pdf` | (missing) |

### candidate_no = SH20271330

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1845` `application_id=1362` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-194/english_certificate/english_certificate-1467348a99574d399816f818f2100fcb.pdf` | (missing) |

### candidate_no = SH20271331

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1627` `application_id=1363` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-549/english_certificate/english_certificate-85bf03957d6d4ad4a954a38dcfc0b891.pdf` | (missing) |

### candidate_no = SH20271332

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1149` `application_id=1364` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1240/english_certificate/english_certificate-32c320a99f34494a8a33a2049cc61cc8.pdf` | (missing) |

### candidate_no = SH20271333

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1358` `application_id=1365` `exam_name=CET-6` `score_text=484` `certificate_attachment_url=/api/v1/portal/attachments/student-941/english_certificate/english_certificate-9d330bcef05c4650baddd65f58c94ddf.pdf` | (missing) |

### candidate_no = SH20271334

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1677` `application_id=1366` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-478/english_certificate/english_certificate-6773d63bee7741d4bbb4a0604ccd86a1.pdf` | (missing) |

### candidate_no = SH20271335

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1525` `application_id=1367` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-705/english_certificate/english_certificate-b4f7b2f3541441b49c3ebbc1e832af75.pdf` | (missing) |

### candidate_no = SH20271336

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=351` `application_id=1368` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2574/english_certificate/english_certificate-04b077389967447c842a9017cf7319b2.jpg` | (missing) |

### candidate_no = SH20271337

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=302` `application_id=1369` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2636/english_certificate/english_certificate-e9535504b30843bbb349a6d7ddab6c2c.pdf` | (missing) |

### candidate_no = SH20271338

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1049` `application_id=1370` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1390/english_certificate/english_certificate-d155b594f2c6420abf065e8a2e5f2366.pdf` | (missing) |

### candidate_no = SH20271339

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=364` `application_id=1371` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2553/english_certificate/english_certificate-67e151e0b6d041bfbe5199ae6923a3ed.pdf` | (missing) |

### candidate_no = SH20271340

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=301` `application_id=1372` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2637/english_certificate/english_certificate-8436f224cb8d4c36861fc1880370680e.pdf` | (missing) |

### candidate_no = SH20271341

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=641` `application_id=1373` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2080/english_certificate/english_certificate-73c0f290ea394a3e9bf9b7700193bcf8.png` | (missing) |

### candidate_no = SH20271342

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=183` `application_id=1374` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2798/english_certificate/english_certificate-e8c94e34085e4614b4b2df9e62163fc1.png` | (missing) |

### candidate_no = SH20271343

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=201` `application_id=1375` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2773/english_certificate/english_certificate-c93a8a24911145e6ace24af37f778003.pdf` | (missing) |

### candidate_no = SH20271344

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=719` `application_id=1376` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1943/english_certificate/english_certificate-49bcc76c3270447d9559ef9834fea719.pdf` | (missing) |

### candidate_no = SH20271345

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=523` `application_id=1377` `exam_name=CET-6` `score_text=580` `certificate_attachment_url=/api/v1/portal/attachments/student-2270/english_certificate/english_certificate-58b7b4ee36e34459b27331d89913fb1c.pdf` | (missing) |

### candidate_no = SH20271346

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1449` `application_id=1378` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-825/english_certificate/english_certificate-016700f1fbb24e75a2fa766c0199f26a.pdf` | (missing) |

### candidate_no = SH20271347

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=679` `application_id=1379` `exam_name=CET-6` `score_text=460` `certificate_attachment_url=/api/v1/portal/attachments/student-2024/english_certificate/english_certificate-fff867df036a4425878b1b6ffee38cef.pdf` | (missing) |

### candidate_no = SH20271348

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=366` `application_id=1380` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2547/english_certificate/english_certificate-d0fa2c09c6e84adc907913b080d62414.pdf` | (missing) |

### candidate_no = SH20271349

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1393` `application_id=1381` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-891/english_certificate/english_certificate-28106aaef49f4fea84b59779aa3c8885.pdf` | (missing) |

### candidate_no = SH20271350

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=325` `application_id=1382` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2606/english_certificate/english_certificate-8216536700d04b5884f1421d653049a2.pdf` | (missing) |

### candidate_no = SH20271351

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=659` `application_id=1383` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2057/english_certificate/english_certificate-0b5f9609a51c46afa874366ea72c6218.pdf` | (missing) |

### candidate_no = SH20271352

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=179` `application_id=1384` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2804/english_certificate/english_certificate-3fdcc113ab834c7980b6d612c2d3d68f.pdf` | (missing) |

### candidate_no = SH20271353

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=196` `application_id=1385` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2778/english_certificate/english_certificate-2d7829c2d35f4072875077f366246c2e.pdf` | (missing) |

### candidate_no = SH20271354

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1346` `application_id=1386` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-962/english_certificate/english_certificate-707afe28dae3457298452e157c7f8f84.pdf` | (missing) |

### candidate_no = SH20271355

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=247` `application_id=1387` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2710/english_certificate/english_certificate-4fb54e20ced242e3a4919730f23bacdb.pdf` | (missing) |

### candidate_no = SH20271356

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=363` `application_id=1388` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2556/english_certificate/english_certificate-01204fa8231f42b386ac745e844dd957.pdf` | (missing) |

### candidate_no = SH20271357

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=611` `application_id=1389` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2136/english_certificate/english_certificate-0ae2ead636404e4e8a54478223c1a85c.pdf` | (missing) |

### candidate_no = SH20271358

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1751` `application_id=1390` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-361/english_certificate/english_certificate-c09e26bebaea4e4fae65a80146cc0027.pdf` | (missing) |

### candidate_no = SH20271359

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=184` `application_id=1391` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2797/english_certificate/english_certificate-927828f4a00440ae9de7f3429c9354bc.pdf` | (missing) |

### candidate_no = SH20271360

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=178` `application_id=1392` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2805/english_certificate/english_certificate-91e7021751274cd49169604ab9d8da1c.pdf` | (missing) |

### candidate_no = SH20271361

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=601` `application_id=1393` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2148/english_certificate/english_certificate-d765e7853d7e4a23a78ea730b7bc648f.png` | (missing) |

### candidate_no = SH20271362

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=929` `application_id=1394` `exam_name=CET-6` `score_text=501` `certificate_attachment_url=/api/v1/portal/attachments/student-1593/english_certificate/english_certificate-c05d80baf1cd40a5b146d8d773b1b02f.pdf` | (missing) |

### candidate_no = SH20271363

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=617` `application_id=1395` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2125/english_certificate/english_certificate-68cc217a75094c51a9e473e36a8b7717.pdf` | (missing) |

### candidate_no = SH20271364

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=190` `application_id=1396` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2788/english_certificate/english_certificate-f6f86327af714b1690669412afda7bd2.pdf` | (missing) |

### candidate_no = SH20271365

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=238` `application_id=1397` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2723/english_certificate/english_certificate-55fc1fffe2084bfa88a917ed02049b5a.pdf` | (missing) |

### candidate_no = SH20271366

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=628` `application_id=1398` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2100/english_certificate/english_certificate-649019f1b7754672b7c727fb4cd3f827.pdf` | (missing) |

### candidate_no = SH20271367

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=563` `application_id=1399` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2213/english_certificate/english_certificate-bd6f9efbc0f34d26bd13a918ecf98462.pdf` | (missing) |

### candidate_no = SH20271368

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=806` `application_id=1400` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1817/english_certificate/english_certificate-f8c4c6b3bc4640a38e76047f81b35850.pdf` | (missing) |

### candidate_no = SH20271369

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=180` `application_id=1401` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2803/english_certificate/english_certificate-54cc6631008045828d338a84f9fa74fb.pdf` | (missing) |

### candidate_no = SH20271370

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1588` `application_id=1402` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-610/english_certificate/english_certificate-fb5f97c41d7c406998ff2458c5e09453.jpg` | (missing) |

### candidate_no = SH20271371

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=187` `application_id=1403` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2791/english_certificate/english_certificate-35d7df0c306b493fa25304a4fd4c49b2.pdf` | (missing) |

### candidate_no = SH20271372

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=324` `application_id=1404` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2607/english_certificate/english_certificate-f09f74e6b0bd49d6acc412da2266533b.pdf` | (missing) |

### candidate_no = SH20271373

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=176` `application_id=1405` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2814/english_certificate/english_certificate-99c9e1f2f092404aa8d98a798bdfb09a.pdf` | (missing) |

### candidate_no = SH20271374

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1837` `application_id=1406` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-206/english_certificate/english_certificate-835d76ce67a0499dba57f7ee79813699.pdf` | (missing) |

### candidate_no = SH20271375

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=213` `application_id=1407` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2757/english_certificate/english_certificate-c6757495c7e948c3a83083ba64723bcd.pdf` | (missing) |

### candidate_no = SH20271376

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=551` `application_id=1408` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2234/english_certificate/english_certificate-5993177fd2b44b3a914c1bc4492423c6.pdf` | (missing) |

### candidate_no = SH20271377

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=273` `application_id=1409` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2675/english_certificate/english_certificate-2d5f47b54e784b7d80e6d2bee1434999.pdf` | (missing) |

### candidate_no = SH20271378

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=820` `application_id=1410` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1796/english_certificate/english_certificate-f74e5731063c41f3bf4d6dc634d6f6cf.pdf` | (missing) |

### candidate_no = SH20271379

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=478` `application_id=1411` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2343/english_certificate/english_certificate-cfbcbfe6ad884a2fb23e8a09e943cfb6.jpg` | (missing) |

### candidate_no = SH20271380

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=714` `application_id=1412` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1959/english_certificate/english_certificate-985f2b74c1b64c549c2438c9e48a5f88.pdf` | (missing) |

### candidate_no = SH20271381

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=861` `application_id=1413` `exam_name=TOEFL` `score_text=106` `certificate_attachment_url=/api/v1/portal/attachments/student-1717/english_certificate/english_certificate-e61fc43cf9b14f91b71aae0e3f7fd567.pdf` | (missing) |
| 第 2 行 | `id=862` `application_id=1413` `exam_name=其他` `score_text=GRE 327` `certificate_attachment_url=/api/v1/portal/attachments/student-1717/english_certificate/english_certificate-d2024df146284bae828674ea0be9966b.pdf` | (missing) |

### candidate_no = SH20271382

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=269` `application_id=1414` `exam_name=CET-6` `score_text=480` `certificate_attachment_url=/api/v1/portal/attachments/student-2680/english_certificate/english_certificate-1b39e5e1ce16439394403be979746008.pdf` | (missing) |

### candidate_no = SH20271383

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=308` `application_id=1415` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2627/english_certificate/english_certificate-d943fbd05fd54e229cf1a1439b9ce63c.pdf` | (missing) |

### candidate_no = SH20271384

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=207` `application_id=1416` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2765/english_certificate/english_certificate-fd07f6324c314bf8823f3544b4c3a20d.pdf` | (missing) |

### candidate_no = SH20271385

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=292` `application_id=1417` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2651/english_certificate/english_certificate-a7f5b6df7ddc46e399ed6e880da55494.pdf` | (missing) |

### candidate_no = SH20271386

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=186` `application_id=1418` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2795/english_certificate/english_certificate-9e370ade9b7749e79ef9bba5a1f5c1d8.pdf` | (missing) |

### candidate_no = SH20271387

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=242` `application_id=1419` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2717/english_certificate/english_certificate-7d1bd8ad26264fc38ba594c5a7a084fd.jpg` | (missing) |

### candidate_no = SH20271388

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=426` `application_id=1420` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2424/english_certificate/english_certificate-bcef69cb8f7f450689621b94f9496be4.pdf` | (missing) |

### candidate_no = SH20271389

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=453` `application_id=1421` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2380/english_certificate/english_certificate-e44e7184bc584072848fb7e681154cea.pdf` | (missing) |

### candidate_no = SH20271390

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=284` `application_id=1422` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2663/english_certificate/english_certificate-d888de82c013463fb40f8230dcbc3e4b.pdf` | (missing) |

### candidate_no = SH20271391

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1527` `application_id=1423` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-703/english_certificate/english_certificate-ccb04b284e4b4b779d240507cd20947f.pdf` | (missing) |

### candidate_no = SH20271392

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=163` `application_id=1424` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2836/english_certificate/english_certificate-cffafb5b47014276baa5e581e23d7960.pdf` | (missing) |

### candidate_no = SH20271393

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=164` `application_id=1425` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2835/english_certificate/english_certificate-53f8d6f55df84f7ba13284f11435f3eb.pdf` | (missing) |

### candidate_no = SH20271394

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1065` `application_id=1426` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1361/english_certificate/english_certificate-233eb9823716428db4c67dccf71c0d9e.pdf` | (missing) |

### candidate_no = SH20271395

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1041` `application_id=1427` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1400/english_certificate/english_certificate-2c6a97188c0a4d1eaba0a8875ff8b2a9.pdf` | (missing) |

### candidate_no = SH20271396

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=445` `application_id=1428` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2390/english_certificate/english_certificate-706f8ed7ab204d2b9a0992ff97e122ba.pdf` | (missing) |

### candidate_no = SH20271397

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=159` `application_id=1429` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2842/english_certificate/english_certificate-1b293adecca64830a0a897b9e678f35e.pdf` | (missing) |

### candidate_no = SH20271398

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=208` `application_id=1430` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2764/english_certificate/english_certificate-cc13eb985adc4a50864e9e43619ec689.pdf` | (missing) |

### candidate_no = SH20271399

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=369` `application_id=1431` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2543/english_certificate/english_certificate-c7d4146250344f2a8984c688bffed15c.jpg` | (missing) |

### candidate_no = SH20271400

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=554` `application_id=1432` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2229/english_certificate/english_certificate-f09416c713864ebd9e93aca46917de66.pdf` | (missing) |

### candidate_no = SH20271401

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=169` `application_id=1433` `exam_name=CET-6` `score_text=443` `certificate_attachment_url=/api/v1/portal/attachments/student-2824/english_certificate/english_certificate-29fd4e250706488ead51ebbdcef53995.pdf` | (missing) |

### candidate_no = SH20271402

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=375` `application_id=1434` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2536/english_certificate/english_certificate-679f1b4b800a4530b2588ba6e75cf4d1.pdf` | (missing) |

### candidate_no = SH20271403

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1460` `application_id=1435` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-804/english_certificate/english_certificate-7eb11835f8674788a7c792a266ffe6a4.pdf` | (missing) |

### candidate_no = SH20271404

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=262` `application_id=1436` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2689/english_certificate/english_certificate-cd0781df551e40b6a71c122b12816c67.pdf` | (missing) |

### candidate_no = SH20271405

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=233` `application_id=1437` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2730/english_certificate/english_certificate-ed699a45a9ef4662bd6c7e8b2a6d47de.pdf` | (missing) |

### candidate_no = SH20271406

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=642` `application_id=1438` `exam_name=TOEFL` `score_text=4.0` `certificate_attachment_url=/api/v1/portal/attachments/student-2079/english_certificate/english_certificate-60f94ba0d4a045609710bdeb0782f074.pdf` | (missing) |

### candidate_no = SH20271407

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=515` `application_id=1439` `exam_name=CET-6` `score_text=451` `certificate_attachment_url=/api/v1/portal/attachments/student-2281/english_certificate/english_certificate-1966d30dfa254d34a1886804caa4dc8f.pdf` | (missing) |

### candidate_no = SH20271408

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=157` `application_id=1440` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2844/english_certificate/english_certificate-225a983af53a4c71861fd96a5d36f1e1.png` | (missing) |

### candidate_no = SH20271409

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=973` `application_id=1441` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1514/english_certificate/english_certificate-a863564f4c244125bdc0023bf92877ac.pdf` | (missing) |

### candidate_no = SH20271410

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1686` `application_id=1442` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-466/english_certificate/english_certificate-7f5e684cb9d14d62935e85daf00788bc.pdf` | (missing) |

### candidate_no = SH20271411

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1089` `application_id=1443` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1323/english_certificate/english_certificate-8212d15a17d8406dab3b36c5d50ac4d7.pdf` | (missing) |

### candidate_no = SH20271412

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=161` `application_id=1444` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2840/english_certificate/english_certificate-f899149b0486441e9f68018b101a19d9.pdf` | (missing) |

### candidate_no = SH20271413

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=229` `application_id=1445` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2734/english_certificate/english_certificate-728376a7c3a344d4b73db96a2ddb32b2.pdf` | (missing) |

### candidate_no = SH20271414

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1328` `application_id=1446` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-983/english_certificate/english_certificate-43cc52dcd9074eeaafbe3c79a2b21c28.png` | (missing) |

### candidate_no = SH20271415

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=469` `application_id=1447` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2356/english_certificate/english_certificate-014399dc398f4a6caad3ae5452f7c58f.pdf` | (missing) |

### candidate_no = SH20271416

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=968` `application_id=1448` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1522/english_certificate/english_certificate-9cb3e869950c4fd89e58903eecdb7e26.pdf` | (missing) |

### candidate_no = SH20271417

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=240` `application_id=1449` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2719/english_certificate/english_certificate-269762a4838946c582b890860d5f21b0.pdf` | (missing) |

### candidate_no = SH20271418

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=378` `application_id=1450` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2531/english_certificate/english_certificate-130f312ab3264363972888e3581d1b57.pdf` | (missing) |

### candidate_no = SH20271419

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1486` `application_id=1451` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-766/english_certificate/english_certificate-caca2546a49b4988b5d7829d3b2c49aa.pdf` | (missing) |

### candidate_no = SH20271420

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1202` `application_id=1452` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1152/english_certificate/english_certificate-22f6d04b421e4545903242ceac5a8ff0.pdf` | (missing) |

### candidate_no = SH20271421

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=268` `application_id=1453` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2681/english_certificate/english_certificate-ec32a381ac064a33b29f516263c9b262.pdf` | (missing) |

### candidate_no = SH20271422

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1906` `application_id=1454` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-107/english_certificate/english_certificate-d0684b79fcf74024b3fd470e68f48801.pdf` | (missing) |

### candidate_no = SH20271423

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=822` `application_id=1455` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1793/english_certificate/english_certificate-cd4289ff44d04b17aa4faa4b8aa67b3a.pdf` | (missing) |

### candidate_no = SH20271424

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=379` `application_id=1456` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2530/english_certificate/english_certificate-e6ed5b53d87b484688f49b2667a7fd4c.pdf` | (missing) |

### candidate_no = SH20271425

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=405` `application_id=1457` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2478/english_certificate/english_certificate-cd9e7182f6544adaba0ef8900f52c18b.pdf` | (missing) |

### candidate_no = SH20271426

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=165` `application_id=1458` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2834/english_certificate/english_certificate-5ee78d0f85134d13882a099f16efa365.pdf` | (missing) |

### candidate_no = SH20271427

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=145` `application_id=1459` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2861/english_certificate/english_certificate-33eeabeabc2d4a269dd7fccf0602ee12.pdf` | (missing) |

### candidate_no = SH20271428

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1592` `application_id=1460` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-604/english_certificate/english_certificate-8de747f4cac64100af0ecbef4d428db1.pdf` | (missing) |

### candidate_no = SH20271429

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=694` `application_id=1461` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1992/english_certificate/english_certificate-e2823f88bb0c42cab24036e544309c89.pdf` | (missing) |

### candidate_no = SH20271430

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1862` `application_id=1462` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-168/english_certificate/english_certificate-75c3c2d9db9b4fefbf70624564188717.pdf` | (missing) |

### candidate_no = SH20271431

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=904` `application_id=1463` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1637/english_certificate/english_certificate-83fa532e73ad4ad580fb7c2be1d3af4e.pdf` | (missing) |

### candidate_no = SH20271432

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1061` `application_id=1464` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1369/english_certificate/english_certificate-65ec55866ba04456850936251909fd48.pdf` | (missing) |

### candidate_no = SH20271433

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=256` `application_id=1465` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2698/english_certificate/english_certificate-0ef59eedd2f141d5abb473f8cd8aed3b.pdf` | (missing) |

### candidate_no = SH20271434

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1066` `application_id=1466` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1358/english_certificate/english_certificate-4d49d3ad362c4c6db453f6994561c494.png` | (missing) |

### candidate_no = SH20271435

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=266` `application_id=1467` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2684/english_certificate/english_certificate-58f705ee1b54405bb0ffc18d57c66d7c.pdf` | (missing) |

### candidate_no = SH20271436

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=139` `application_id=1468` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2869/english_certificate/english_certificate-c52b1b4e16ed4af98b94d1507ddee9b9.jpeg` | (missing) |

### candidate_no = SH20271437

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=347` `application_id=1469` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2578/english_certificate/english_certificate-71facd8fc25741a5b927d310a38368c1.pdf` | (missing) |

### candidate_no = SH20271438

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=272` `application_id=1470` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2676/english_certificate/english_certificate-7eefdc77b0dd46dea6fa4cc7a6393e10.pdf` | (missing) |

### candidate_no = SH20271439

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1378` `application_id=1471` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-910/english_certificate/english_certificate-fe89785124c644c09e1a89e631f1aeb4.pdf` | (missing) |

### candidate_no = SH20271440

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=643` `application_id=1472` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2076/english_certificate/english_certificate-be1c623b9667405d9322048224222c2b.pdf` | (missing) |

### candidate_no = SH20271441

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=602` `application_id=1473` `exam_name=CET-6` `score_text=615` `certificate_attachment_url=/api/v1/portal/attachments/student-2147/english_certificate/english_certificate-4e9900bfbc0d4e18a499667714f701a5.pdf` | (missing) |
| 第 2 行 | `id=603` `application_id=1473` `exam_name=TOEFL` `score_text=105` `certificate_attachment_url=/api/v1/portal/attachments/student-2147/english_certificate/english_certificate-f2e944ceb6404c139a1a9178eb0a39d9.pdf` | (missing) |

### candidate_no = SH20271442

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=383` `application_id=1474` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2519/english_certificate/english_certificate-ca0fe30e760e434484a263035f71d1fd.png` | (missing) |

### candidate_no = SH20271443

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=467` `application_id=1475` `exam_name=CET-6` `score_text=652` `certificate_attachment_url=/api/v1/portal/attachments/student-2358/english_certificate/english_certificate-32360325d29542558ea25567588678ac.pdf` | (missing) |
| 第 2 行 | `id=468` `application_id=1475` `exam_name=TOEFL` `score_text=109` `certificate_attachment_url=/api/v1/portal/attachments/student-2358/english_certificate/english_certificate-2f37d02f8cce487bae9b8e1e9eb5f7c7.pdf` | (missing) |

### candidate_no = SH20271444

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1490` `application_id=1476` `exam_name=CET-6` `score_text=481` `certificate_attachment_url=/api/v1/portal/attachments/student-758/english_certificate/english_certificate-a84364fd690f4461a94ae3f9119c0b66.pdf` | (missing) |

### candidate_no = SH20271445

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1062` `application_id=1477` `exam_name=CET-6` `score_text=565` `certificate_attachment_url=/api/v1/portal/attachments/student-1368/english_certificate/english_certificate-122d8e6cf52348598634dc65b4fd35d2.pdf` | (missing) |

### candidate_no = SH20271446

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=198` `application_id=1478` `exam_name=CET-6` `score_text=547` `certificate_attachment_url=/api/v1/portal/attachments/student-2776/english_certificate/english_certificate-a7cf48fec142457e8f50c42d11307743.pdf` | (missing) |

### candidate_no = SH20271447

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=476` `application_id=1479` `exam_name=CET-6` `score_text=525` `certificate_attachment_url=/api/v1/portal/attachments/student-2345/english_certificate/english_certificate-674ba535e2544b54b7c810a6439bb669.pdf` | (missing) |

### candidate_no = SH20271448

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=333` `application_id=1480` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2597/english_certificate/english_certificate-c7d9e7ff69a544fb88bdad9cb400c903.pdf` | (missing) |

### candidate_no = SH20271449

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=225` `application_id=1481` `exam_name=CET-6` `score_text=426` `certificate_attachment_url=/api/v1/portal/attachments/student-2738/english_certificate/english_certificate-ff13a4be93b24be4969829a0b1db88c9.pdf` | (missing) |

### candidate_no = SH20271450

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=664` `application_id=1482` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2049/english_certificate/english_certificate-180367ed899b40b98ec643cb6c6bd6ae.pdf` | (missing) |

### candidate_no = SH20271451

- 主库行数：3
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1361` `application_id=1483` `exam_name=CET-6` `score_text=600` `certificate_attachment_url=/api/v1/portal/attachments/student-938/english_certificate/english_certificate-b9988ef91c7d419db100ba279f29ce0e.pdf` | (missing) |
| 第 2 行 | `id=1362` `application_id=1483` `exam_name=TOEFL` `score_text=95` `certificate_attachment_url=/api/v1/portal/attachments/student-938/english_certificate/english_certificate-b11a9d3d874b4f78972ec3c1080651a5.pdf` | (missing) |
| 第 3 行 | `id=1363` `application_id=1483` `exam_name=其他` `score_text=607（CET-4）` `certificate_attachment_url=/api/v1/portal/attachments/student-938/english_certificate/english_certificate-95a818f389474ed988cab22ff2967856.pdf` | (missing) |

### candidate_no = SH20271452

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=700` `application_id=1484` `exam_name=CET-6` `score_text=529` `certificate_attachment_url=/api/v1/portal/attachments/student-1979/english_certificate/english_certificate-2bcd2d968a5d4e28970cbd7b4fe34d30.pdf` | (missing) |

### candidate_no = SH20271453

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1352` `application_id=1485` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-948/english_certificate/english_certificate-d4e9c55cf6b24f24abb3923dc96d8bde.pdf` | (missing) |

### candidate_no = SH20271454

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=726` `application_id=1486` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1933/english_certificate/english_certificate-c9ee5020c11a48ff914ef7db65ac25d7.pdf` | (missing) |

### candidate_no = SH20271455

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=567` `application_id=1487` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2207/english_certificate/english_certificate-74ae33b965b84d02a86f9d1c5128f687.pdf` | (missing) |

### candidate_no = SH20271456

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1295` `application_id=1488` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1030/english_certificate/english_certificate-f0e46c293f9f41d1988ec1e1ca1a74e6.pdf` | (missing) |

### candidate_no = SH20271457

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=399` `application_id=1489` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2488/english_certificate/english_certificate-3019661e19bc4d9994b84df51e969ae8.pdf` | (missing) |

### candidate_no = SH20271458

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=566` `application_id=1490` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2208/english_certificate/english_certificate-97e7a6b0875c44679fecd457c6b31ec8.pdf` | (missing) |

### candidate_no = SH20271459

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1424` `application_id=1491` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-855/english_certificate/english_certificate-54366f09f99a43068acdf33b8c4b64ac.pdf` | (missing) |

### candidate_no = SH20271460

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=125` `application_id=1492` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2888/english_certificate/english_certificate-c72115f206a74dfc910f4afa0e3916ff.pdf` | (missing) |

### candidate_no = SH20271461

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=126` `application_id=1493` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2887/english_certificate/english_certificate-a3b8533b46c14a2e9d9de059216a4bcf.pdf` | (missing) |

### candidate_no = SH20271462

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=257` `application_id=1494` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2697/english_certificate/english_certificate-cc51169d34e540ad88b778bd1556b33e.pdf` | (missing) |

### candidate_no = SH20271463

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=138` `application_id=1495` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2871/english_certificate/english_certificate-50c4ec4642ec4401a0f001744b68f89b.pdf` | (missing) |

### candidate_no = SH20271464

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=465` `application_id=1496` `exam_name=CET-6` `score_text=563` `certificate_attachment_url=/api/v1/portal/attachments/student-2360/english_certificate/english_certificate-c318c82ee077402cbf7e595701a21cb3.pdf` | (missing) |

### candidate_no = SH20271465

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1036` `application_id=1497` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1413/english_certificate/english_certificate-476f63720c024522b8a90239c2207bc7.pdf` | (missing) |

### candidate_no = SH20271466

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=834` `application_id=1498` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1766/english_certificate/english_certificate-420b2cfc25244c67bb1a17bb3f20f235.pdf` | (missing) |

### candidate_no = SH20271467

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1404` `application_id=1499` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-879/english_certificate/english_certificate-9778d1ffb58f4e80a1c6ed52978dff6b.pdf` | (missing) |

### candidate_no = SH20271468

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1420` `application_id=1500` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-859/english_certificate/english_certificate-cabf8bbfe05f417b9bc223a1afa536d9.pdf` | (missing) |

### candidate_no = SH20271469

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=671` `application_id=1501` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2038/english_certificate/english_certificate-e77dcc092e594e048a0057f49651ca9b.pdf` | (missing) |

### candidate_no = SH20271470

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=152` `application_id=1502` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2852/english_certificate/english_certificate-fa879f00afd84d7fa884fd7cae98f376.pdf` | (missing) |

### candidate_no = SH20271471

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=166` `application_id=1503` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2832/english_certificate/english_certificate-06bdefa741624ef7bb99f5f8e5c60915.pdf` | (missing) |

### candidate_no = SH20271472

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=275` `application_id=1504` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2673/english_certificate/english_certificate-b986da23a1f444e4888c65597de9e534.pdf` | (missing) |

### candidate_no = SH20271473

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1003` `application_id=1505` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1466/english_certificate/english_certificate-f0ffd3823f9f43368f936947fa052815.png` | (missing) |

### candidate_no = SH20271474

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=124` `application_id=1506` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2891/english_certificate/english_certificate-02918a0b4ed14d43af41e5916baaa50e.pdf` | (missing) |

### candidate_no = SH20271475

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1364` `application_id=1507` `exam_name=CET-6` `score_text=465` `certificate_attachment_url=/api/v1/portal/attachments/student-936/english_certificate/english_certificate-145f39360a574e1f83a7f64387aae0f2.pdf` | (missing) |

### candidate_no = SH20271476

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=456` `application_id=1508` `exam_name=CET-6` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-2376/english_certificate/english_certificate-dddb05a601e74db0b74776f3c04566c8.pdf` | (missing) |

### candidate_no = SH20271477

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=342` `application_id=1509` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2585/english_certificate/english_certificate-dd50660234e74c8ba529fd8f2e240d4b.jpg` | (missing) |

### candidate_no = SH20271478

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1617` `application_id=1510` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-564/english_certificate/english_certificate-c0ca5ce989564a7a9dea0ba3b05f1d86.pdf` | (missing) |

### candidate_no = SH20271479

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1212` `application_id=1511` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1134/english_certificate/english_certificate-e8a94baa27074c56a94cbd2703b939bd.pdf` | (missing) |

### candidate_no = SH20271480

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=127` `application_id=1512` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2886/english_certificate/english_certificate-bf826ed228a34516ae5860cef4ccab64.pdf` | (missing) |

### candidate_no = SH20271481

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=408` `application_id=1513` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2469/english_certificate/english_certificate-d6f0ca9a9f654b7e9f08b52abbd93526.pdf` | (missing) |

### candidate_no = SH20271482

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1712` `application_id=1514` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-424/english_certificate/english_certificate-a9f9f634566243e1bfa9cf82d3103089.pdf` | (missing) |

### candidate_no = SH20271483

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=853` `application_id=1515` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1730/english_certificate/english_certificate-60436e962c1f4808900a2b850cd963e3.pdf` | (missing) |

### candidate_no = SH20271484

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1406` `application_id=1516` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-875/english_certificate/english_certificate-c8008f12f3ae455abd928ab806fe86fa.pdf` | (missing) |

### candidate_no = SH20271485

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=135` `application_id=1517` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2877/english_certificate/english_certificate-40c3f6b4fb454d728586ed00e948d3bf.pdf` | (missing) |

### candidate_no = SH20271486

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=160` `application_id=1518` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2841/english_certificate/english_certificate-0ca79c498c3c44e6be5a28e05bf9a91b.pdf` | (missing) |

### candidate_no = SH20271487

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=969` `application_id=1519` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1521/english_certificate/english_certificate-e250505175b94251b7e2d70ee2eca137.pdf` | (missing) |

### candidate_no = SH20271488

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1888` `application_id=1520` `exam_name=CET-6` `score_text=527` `certificate_attachment_url=/api/v1/portal/attachments/student-131/english_certificate/english_certificate-59656d3712074bfba623d32c3cbea7e4.pdf` | (missing) |

### candidate_no = SH20271489

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=905` `application_id=1521` `exam_name=CET-6` `score_text=595` `certificate_attachment_url=/api/v1/portal/attachments/student-1635/english_certificate/english_certificate-434bd40e27eb45cda96502a8e8387b87.png` | (missing) |

### candidate_no = SH20271490

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=447` `application_id=1522` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2388/english_certificate/english_certificate-f9614f849cb24d6998f30ab68499b3d0.pdf` | (missing) |

### candidate_no = SH20271491

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=210` `application_id=1523` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2760/english_certificate/english_certificate-c5928874d9b74d7b963efda2f5b1eaa0.pdf` | (missing) |

### candidate_no = SH20271492

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1501` `application_id=1524` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-747/english_certificate/english_certificate-f348c507f02649d1bd45e48742358651.pdf` | (missing) |

### candidate_no = SH20271493

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=945` `application_id=1525` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1568/english_certificate/english_certificate-562f38bf091a4864866499ebe4329e49.png` | (missing) |

### candidate_no = SH20271494

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1259` `application_id=1526` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1070/english_certificate/english_certificate-a1801215e4a145d886a3cd6b8e174b17.pdf` | (missing) |

### candidate_no = SH20271495

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=940` `application_id=1527` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1576/english_certificate/english_certificate-11755681d0934e2fbb82f3e35f845af5.pdf` | (missing) |

### candidate_no = SH20271496

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=638` `application_id=1528` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2087/english_certificate/english_certificate-b8650934db5c476684a5df1f4bf3b9fd.pdf` | (missing) |

### candidate_no = SH20271497

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=936` `application_id=1529` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1580/english_certificate/english_certificate-1fa32a167822497793329e17f1e92855.pdf` | (missing) |

### candidate_no = SH20271498

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=148` `application_id=1530` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2857/english_certificate/english_certificate-f7f7ef2063f64886acd2aed81d4d4df5.pdf` | (missing) |

### candidate_no = SH20271499

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1932` `application_id=1531` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-74/english_certificate/english_certificate-664615a088144e739e52cabe8f40432c.jpg` | (missing) |

### candidate_no = SH20271500

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1456` `application_id=1532` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-814/english_certificate/english_certificate-0f2f90861a59421abb5713cbb86f0346.pdf` | (missing) |

### candidate_no = SH20271501

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=522` `application_id=1533` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2273/english_certificate/english_certificate-3216606d17bb4036a5179f9e70d0be71.pdf` | (missing) |

### candidate_no = SH20271502

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1613` `application_id=1534` `exam_name=IELTS` `score_text=6` `certificate_attachment_url=/api/v1/portal/attachments/student-570/english_certificate/english_certificate-0a2bdef222ac4331983e01d29b95b6fb.pdf` | (missing) |

### candidate_no = SH20271503

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=216` `application_id=1535` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2753/english_certificate/english_certificate-750636133dd34c818fdcb8cf15f376b3.pdf` | (missing) |

### candidate_no = SH20271504

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=131` `application_id=1536` `exam_name=CET-6` `score_text=409` `certificate_attachment_url=/api/v1/portal/attachments/student-2882/english_certificate/english_certificate-57f28477c5b8405a9099d43fa86068e7.pdf` | (missing) |

### candidate_no = SH20271505

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1669` `application_id=1537` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-489/english_certificate/english_certificate-602f1a805b6049008327baf666a7ae22.pdf` | (missing) |

### candidate_no = SH20271506

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=129` `application_id=1538` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2884/english_certificate/english_certificate-08dd4a4981374bdf97cfe9853eeffbe8.pdf` | (missing) |

### candidate_no = SH20271507

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1169` `application_id=1539` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1208/english_certificate/english_certificate-477e3146a98b46ecaee5696508cf32a6.pdf` | (missing) |

### candidate_no = SH20271508

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=206` `application_id=1540` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2766/english_certificate/english_certificate-8d270a1b2ea04918af8dbb60cab07fb4.pdf` | (missing) |

### candidate_no = SH20271509

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1517` `application_id=1541` `exam_name=CET-6` `score_text=611` `certificate_attachment_url=/api/v1/portal/attachments/student-721/english_certificate/english_certificate-36d44ebdbd944f9aa2de0593026bc5e6.pdf` | (missing) |

### candidate_no = SH20271510

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=117` `application_id=1542` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2900/english_certificate/english_certificate-aa3b9e43cda344fb99d5c22acff01660.pdf` | (missing) |

### candidate_no = SH20271511

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=134` `application_id=1543` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2878/english_certificate/english_certificate-19db1d7ce6cb4588988f701818a0ec4c.jpg` | (missing) |

### candidate_no = SH20271512

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=142` `application_id=1544` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2866/english_certificate/english_certificate-7db11152f3ca4bd5b2d4039dfaacb760.pdf` | (missing) |

### candidate_no = SH20271513

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=249` `application_id=1545` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2708/english_certificate/english_certificate-8d31241edffb46bb9d24ac0b3011caf1.pdf` | (missing) |

### candidate_no = SH20271514

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=114` `application_id=1546` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2903/english_certificate/english_certificate-67b123dbbdf448a58b481eee62674bdb.pdf` | (missing) |

### candidate_no = SH20271515

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=192` `application_id=1547` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2785/english_certificate/english_certificate-11f8b15ef0cb4ecb9945c9254f9d1b37.png` | (missing) |

### candidate_no = SH20271516

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1427` `application_id=1548` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-852/english_certificate/english_certificate-07319505e60140fcbec078806d58d7d8.pdf` | (missing) |

### candidate_no = SH20271517

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1084` `application_id=1549` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1330/english_certificate/english_certificate-394793cedebe419e91ed11fcdcff24ba.png` | (missing) |

### candidate_no = SH20271518

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=352` `application_id=1550` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2571/english_certificate/english_certificate-a4a857c7fa554ac787f20d92daadd4fa.pdf` | (missing) |

### candidate_no = SH20271519

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=197` `application_id=1551` `exam_name=CET-6` `score_text=530` `certificate_attachment_url=/api/v1/portal/attachments/student-2777/english_certificate/english_certificate-06fc818ab2b84e51aee0d7d092c313b3.pdf` | (missing) |

### candidate_no = SH20271520

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=762` `application_id=1552` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1872/english_certificate/english_certificate-28456985d3cb44feae61b8f81fd245d6.pdf` | (missing) |

### candidate_no = SH20271521

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=230` `application_id=1553` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2733/english_certificate/english_certificate-8affe61bb9214f61ac183ac69eb43514.jpg` | (missing) |

### candidate_no = SH20271522

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1076` `application_id=1554` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1344/english_certificate/english_certificate-b90034d869564d5ea30b3b10b1f61d4a.pdf` | (missing) |

### candidate_no = SH20271523

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=111` `application_id=1555` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2906/english_certificate/english_certificate-5539adc0dcbc47b499c4f1643f009ac7.jpg` | (missing) |

### candidate_no = SH20271524

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=220` `application_id=1556` `exam_name=CET-6` `score_text=400` `certificate_attachment_url=/api/v1/portal/attachments/student-2744/english_certificate/english_certificate-d1483ee5581d48479deb9c0402de3026.pdf` | (missing) |
| 第 2 行 | `id=221` `application_id=1556` `exam_name=其他` `score_text=474` `certificate_attachment_url=/api/v1/portal/attachments/student-2744/english_certificate/english_certificate-dd1008db0dfd4ca48141841e1390b5c8.pdf` | (missing) |

### candidate_no = SH20271525

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=250` `application_id=1557` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2707/english_certificate/english_certificate-6cfecb8710e944809d0f9761e69f1280.pdf` | (missing) |

### candidate_no = SH20271526

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=234` `application_id=1558` `exam_name=CET-6` `score_text=480` `certificate_attachment_url=/api/v1/portal/attachments/student-2729/english_certificate/english_certificate-d0fac861ccf9436eabe620995314454c.pdf` | (missing) |

### candidate_no = SH20271527

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=470` `application_id=1559` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2354/english_certificate/english_certificate-5d6c835275fa4e78829d5833c353ed9e.pdf` | (missing) |

### candidate_no = SH20271528

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=175` `application_id=1560` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2815/english_certificate/english_certificate-45c1b4854bb14b3fb02b8fea2be1a115.pdf` | (missing) |

### candidate_no = SH20271529

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=574` `application_id=1561` `exam_name=CET-6` `score_text=479` `certificate_attachment_url=/api/v1/portal/attachments/student-2200/english_certificate/english_certificate-161e701e60ad42cf8ccc25265cecdbfa.pdf` | (missing) |

### candidate_no = SH20271530

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=817` `application_id=1562` `exam_name=CET-6` `score_text=511` `certificate_attachment_url=/api/v1/portal/attachments/student-1802/english_certificate/english_certificate-29437194789545ea8b23fa351895237f.pdf` | (missing) |

### candidate_no = SH20271531

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1741` `application_id=1563` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-378/english_certificate/english_certificate-7333755ddace4289a2d901b477a590b4.pdf` | (missing) |

### candidate_no = SH20271532

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=444` `application_id=1564` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2391/english_certificate/english_certificate-f46e585d4bb245a98ddaa0aa3eb39a9a.pdf` | (missing) |

### candidate_no = SH20271533

- 主库行数：4
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=318` `application_id=1565` `exam_name=CET-6` `score_text=618` `certificate_attachment_url=/api/v1/portal/attachments/student-2610/english_certificate/english_certificate-7785cf17e265464ba47c58904acf2ef3.jpg` | (missing) |
| 第 2 行 | `id=319` `application_id=1565` `exam_name=其他` `score_text=2024年全国大学生英语竞赛（NECCS）国家级C类二等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-2610/english_certificate/english_certificate-f73fd3ba99ad448ab9c9256efb9132f2.jpg` | (missing) |
| 第 3 行 | `id=320` `application_id=1565` `exam_name=其他` `score_text=2024“外研社·国才杯”“理解当代中国”全国大学生外语能力大赛英语组国际传播综合能力赛项国家级铜奖` `certificate_attachment_url=/api/v1/portal/attachments/student-2610/english_certificate/english_certificate-6fca394bf42946d9b32b8e038315393b.jpg` | (missing) |
| 第 4 行 | `id=321` `application_id=1565` `exam_name=其他` `score_text=2024年 国际人才英语考试（高级）良好等级` `certificate_attachment_url=/api/v1/portal/attachments/student-2610/english_certificate/english_certificate-2f132b2c51a64765945240b9d5f548d4.jpg` | (missing) |

### candidate_no = SH20271534

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=621` `application_id=1566` `exam_name=CET-6` `score_text=479` `certificate_attachment_url=/api/v1/portal/attachments/student-2115/english_certificate/english_certificate-7a9d7374986346a68e47bfe2fd6dba9a.pdf` | (missing) |

### candidate_no = SH20271535

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=167` `application_id=1567` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2831/english_certificate/english_certificate-a4a557eb04b7411f980c9633106bc8ca.pdf` | (missing) |

### candidate_no = SH20271536

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=102` `application_id=1568` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2920/english_certificate/english_certificate-9e5c5762c33345df9f5a15af425d0597.pdf` | (missing) |

### candidate_no = SH20271537

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1512` `application_id=1569` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-728/english_certificate/english_certificate-64134e7164654c2ca61b1933cfaa1f82.pdf` | (missing) |

### candidate_no = SH20271538

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=828` `application_id=1570` `exam_name=CET-6` `score_text=516` `certificate_attachment_url=/api/v1/portal/attachments/student-1781/english_certificate/english_certificate-bd64b6be264c4a29bfc746c58bacc5d6.pdf` | (missing) |

### candidate_no = SH20271539

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=94` `application_id=1571` `exam_name=CET-6` `score_text=602` `certificate_attachment_url=/api/v1/portal/attachments/student-2934/english_certificate/english_certificate-5a15657f25cf498890c6c54700cf6dca.pdf` | (missing) |

### candidate_no = SH20271540

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=316` `application_id=1572` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2618/english_certificate/english_certificate-4896e4471dc3499f99d95473c1893c7c.pdf` | (missing) |

### candidate_no = SH20271541

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=92` `application_id=1573` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2937/english_certificate/english_certificate-81ed8e8b742c498d8b67dd3400ec137c.pdf` | (missing) |

### candidate_no = SH20271542

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=672` `application_id=1574` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2036/english_certificate/english_certificate-871037a692854299a84d07e0eac86c7e.pdf` | (missing) |

### candidate_no = SH20271543

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=97` `application_id=1575` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2930/english_certificate/english_certificate-4c0d3921e2a446de80d8c618d51b3d53.pdf` | (missing) |

### candidate_no = SH20271544

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1485` `application_id=1576` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-768/english_certificate/english_certificate-198ec79bba2a49259525b976a9a652cf.pdf` | (missing) |

### candidate_no = SH20271545

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1942` `application_id=1577` `exam_name=CET-6` `score_text=548` `certificate_attachment_url=/api/v1/portal/attachments/student-59/english_certificate/english_certificate-7b8a66879270408d8168e5665544c34c.pdf` | (missing) |

### candidate_no = SH20271546

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=287` `application_id=1578` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2658/english_certificate/english_certificate-0d19ca6c0bad481586319f617db88e8b.pdf` | (missing) |

### candidate_no = SH20271547

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=259` `application_id=1579` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2694/english_certificate/english_certificate-1cb63be880e64106b2efd8cc7faef232.pdf` | (missing) |

### candidate_no = SH20271548

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1851` `application_id=1580` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-182/english_certificate/english_certificate-bc5cf29ba56e4639b00b50c4e74c47b2.pdf` | (missing) |

### candidate_no = SH20271549

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=84` `application_id=1581` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2951/english_certificate/english_certificate-666cb935054d4efeb75aa0e3ff0d4c9f.pdf` | (missing) |

### candidate_no = SH20271550

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=296` `application_id=1582` `exam_name=CET-6` `score_text=495` `certificate_attachment_url=/api/v1/portal/attachments/student-2642/english_certificate/english_certificate-53c0d08f898649cfb54ec21d87099c54.pdf` | (missing) |

### candidate_no = SH20271551

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1103` `application_id=1583` `exam_name=CET-6` `score_text=466` `certificate_attachment_url=/api/v1/portal/attachments/student-1303/english_certificate/english_certificate-85669f5d6dcf492ca53ca56176f52c0c.pdf` | (missing) |
| 第 2 行 | `id=1104` `application_id=1583` `exam_name=其他` `score_text=638` `certificate_attachment_url=/api/v1/portal/attachments/student-1303/english_certificate/english_certificate-e150ed50b8ce4391b36a99342ec0e75c.pdf` | (missing) |

### candidate_no = SH20271552

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=713` `application_id=1584` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1960/english_certificate/english_certificate-c15cfdc50da74243a3f8d862b976918f.pdf` | (missing) |

### candidate_no = SH20271553

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=393` `application_id=1585` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2497/english_certificate/english_certificate-ce48df2aa87b4ece800607b1019e7a49.pdf` | (missing) |

### candidate_no = SH20271554

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1719` `application_id=1586` `exam_name=其他` `score_text=557` `certificate_attachment_url=/api/v1/portal/attachments/student-413/english_certificate/english_certificate-20f86447b72b491797422c795d076944.pdf` | (missing) |

### candidate_no = SH20271555

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=93` `application_id=1587` `exam_name=CET-6` `score_text=479` `certificate_attachment_url=/api/v1/portal/attachments/student-2936/english_certificate/english_certificate-9bc8aa2b5d6f4a2e9a8ea86999c90d6e.pdf` | (missing) |

### candidate_no = SH20271556

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=79` `application_id=1588` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-2956/english_certificate/english_certificate-b0aa72d2ca1342078482501f814a81c9.pdf` | (missing) |

### candidate_no = SH20271557

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=448` `application_id=1589` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2386/english_certificate/english_certificate-3819ab37f8fc4351bb8fb2fc44982b46.pdf` | (missing) |

### candidate_no = SH20271558

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=343` `application_id=1590` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2582/english_certificate/english_certificate-c9025df133c9418e901dfd56be70c1de.pdf` | (missing) |

### candidate_no = SH20271559

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=830` `application_id=1591` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1776/english_certificate/english_certificate-b22453f3f1444c52b7a2be712add3347.pdf` | (missing) |

### candidate_no = SH20271560

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1722` `application_id=1592` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-410/english_certificate/english_certificate-db7a47b843d9411a832da8cb01538f3a.pdf` | (missing) |

### candidate_no = SH20271561

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1767` `application_id=1593` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-330/english_certificate/english_certificate-3720f7e20c79433689c4dc578788ee95.pdf` | (missing) |

### candidate_no = SH20271562

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=86` `application_id=1594` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2946/english_certificate/english_certificate-e2b7589903714c86a497cb77e28d6311.pdf` | (missing) |

### candidate_no = SH20271563

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=78` `application_id=1595` `exam_name=CET-6` `score_text=559` `certificate_attachment_url=/api/v1/portal/attachments/student-2957/english_certificate/english_certificate-4869405f3d7f4e2b84bafe3ca6a708be.pdf` | (missing) |

### candidate_no = SH20271564

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=177` `application_id=1596` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2813/english_certificate/english_certificate-fe82fc3398cc414aba50412d7e893e84.jpg` | (missing) |

### candidate_no = SH20271565

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=891` `application_id=1597` `exam_name=CET-6` `score_text=495` `certificate_attachment_url=/api/v1/portal/attachments/student-1665/english_certificate/english_certificate-40e65747679d4018a111ffc8a6ea7511.pdf` | (missing) |

### candidate_no = SH20271566

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=81` `application_id=1598` `exam_name=CET-6` `score_text=639` `certificate_attachment_url=/api/v1/portal/attachments/student-2953/english_certificate/english_certificate-08463deef24549c7895665070f8f304b.pdf` | (missing) |
| 第 2 行 | `id=82` `application_id=1598` `exam_name=其他` `score_text=671` `certificate_attachment_url=/api/v1/portal/attachments/student-2953/english_certificate/english_certificate-cc1aa109787246ccb15ee61a9613b958.pdf` | (missing) |

### candidate_no = SH20271567

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=137` `application_id=1599` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2872/english_certificate/english_certificate-ce349932e15a4428a989d720300267e9.png` | (missing) |

### candidate_no = SH20271568

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=800` `application_id=1600` `exam_name=CET-6` `score_text=511` `certificate_attachment_url=/api/v1/portal/attachments/student-1823/english_certificate/english_certificate-9644cf83a73f4b46a904b1a9f553e50a.png` | (missing) |

### candidate_no = SH20271569

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=441` `application_id=1601` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2394/english_certificate/english_certificate-e8b36b4228354c39b73cbc7e351a5740.pdf` | (missing) |

### candidate_no = SH20271570

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=76` `application_id=1602` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2959/english_certificate/english_certificate-3ad2e2d4d7f546bf8a86f5d4a66257ac.pdf` | (missing) |

### candidate_no = SH20271571

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1281` `application_id=1603` `exam_name=CET-6` `score_text=540` `certificate_attachment_url=/api/v1/portal/attachments/student-1046/english_certificate/english_certificate-5e24a827be9d4c88a53a978764c78010.pdf` | (missing) |
| 第 2 行 | `id=1282` `application_id=1603` `exam_name=其他` `score_text=610` `certificate_attachment_url=/api/v1/portal/attachments/student-1046/english_certificate/english_certificate-b3708393c15a4595a4f0a75b8da2158e.pdf` | (missing) |

### candidate_no = SH20271572

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1502` `application_id=1604` `exam_name=CET-6` `score_text=521` `certificate_attachment_url=/api/v1/portal/attachments/student-745/english_certificate/english_certificate-3581b6bc0e044308945ea69c15c57de3.pdf` | (missing) |

### candidate_no = SH20271573

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=228` `application_id=1605` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2735/english_certificate/english_certificate-5eb0aaefd7c248698da4a3a66fbb7b60.pdf` | (missing) |

### candidate_no = SH20271574

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=77` `application_id=1606` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2958/english_certificate/english_certificate-d221bbe0e0314769a2c64037e45a815b.jpg` | (missing) |

### candidate_no = SH20271575

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=68` `application_id=1607` `exam_name=CET-6` `score_text=429` `certificate_attachment_url=/api/v1/portal/attachments/student-2974/english_certificate/english_certificate-15c397146ae3480e94a64867211b29fa.pdf` | (missing) |

### candidate_no = SH20271576

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=462` `application_id=1608` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2366/english_certificate/english_certificate-210cca84a0884808aa76150a57d7854c.pdf` | (missing) |

### candidate_no = SH20271577

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1702` `application_id=1609` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-442/english_certificate/english_certificate-0b9b3ea2069c4657b412e2c6913a38d1.pdf` | (missing) |

### candidate_no = SH20271578

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=118` `application_id=1610` `exam_name=CET-6` `score_text=574` `certificate_attachment_url=/api/v1/portal/attachments/student-2899/english_certificate/english_certificate-39e39b3ead7c45a7b93c5e88728f94f6.pdf` | (missing) |

### candidate_no = SH20271579

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=455` `application_id=1611` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2377/english_certificate/english_certificate-49ecf2dd225643ac8d233294c722a770.pdf` | (missing) |

### candidate_no = SH20271580

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=73` `application_id=1612` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2964/english_certificate/english_certificate-4fcf479e396a4b84b68bbe7bd9200aa2.pdf` | (missing) |

### candidate_no = SH20271581

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=288` `application_id=1613` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2657/english_certificate/english_certificate-08b6108e4e1a47f783ba12672d097697.pdf` | (missing) |

### candidate_no = SH20271582

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=123` `application_id=1614` `exam_name=CET-6` `score_text=520` `certificate_attachment_url=/api/v1/portal/attachments/student-2892/english_certificate/english_certificate-a188f8e512014c019691c5f73094e9a6.pdf` | (missing) |

### candidate_no = SH20271583

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=651` `application_id=1615` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2066/english_certificate/english_certificate-daf429d021b54418b547b4afe94420a4.pdf` | (missing) |

### candidate_no = SH20271584

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=459` `application_id=1616` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2371/english_certificate/english_certificate-2ce2add87f2d41cebf8ac3ac1855c787.jpg` | (missing) |

### candidate_no = SH20271585

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=572` `application_id=1617` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2202/english_certificate/english_certificate-dadd683dfacb4378b93e3483dc84bd0e.pdf` | (missing) |

### candidate_no = SH20271586

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=652` `application_id=1618` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2065/english_certificate/english_certificate-0df129ed81254342af30749e9bba15cf.jpg` | (missing) |

### candidate_no = SH20271587

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=934` `application_id=1619` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1584/english_certificate/english_certificate-8ebffc0b4b7a46ed8203c6b8fdc1dda9.pdf` | (missing) |

### candidate_no = SH20271588

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=74` `application_id=1620` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2961/english_certificate/english_certificate-e3ca7a3f053e405886f51f5838a11d05.pdf` | (missing) |

### candidate_no = SH20271589

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1567` `application_id=1621` `exam_name=CET-6` `score_text=548` `certificate_attachment_url=/api/v1/portal/attachments/student-638/english_certificate/english_certificate-b369dc158b0f475e9e834c17da811393.pdf` | (missing) |

### candidate_no = SH20271590

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=525` `application_id=1622` `exam_name=CET-6` `score_text=563` `certificate_attachment_url=/api/v1/portal/attachments/student-2268/english_certificate/english_certificate-02bd329d5271455c872f84fa044cbc12.pdf` | (missing) |

### candidate_no = SH20271591

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=61` `application_id=1623` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2987/english_certificate/english_certificate-5dfb06264b24456c9b2daa83c7c26f55.pdf` | (missing) |

### candidate_no = SH20271592

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=108` `application_id=1624` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2912/english_certificate/english_certificate-c4058ec4cd4642d2a1ea1429664a27e4.pdf` | (missing) |

### candidate_no = SH20271593

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1511` `application_id=1625` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-731/english_certificate/english_certificate-f090df110d1945c292182205dc02b10f.jpg` | (missing) |

### candidate_no = SH20271594

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=59` `application_id=1626` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2989/english_certificate/english_certificate-aa77a610cb434057a6f721635a0601f9.pdf` | (missing) |

### candidate_no = SH20271595

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=98` `application_id=1627` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2929/english_certificate/english_certificate-c7d65ff9e6684f4296491956b8d711db.pdf` | (missing) |

### candidate_no = SH20271596

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=112` `application_id=1628` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2905/english_certificate/english_certificate-3d363fd70ce44bd0aed8dd06a7aa4d52.png` | (missing) |

### candidate_no = SH20271597

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=317` `application_id=1629` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2616/english_certificate/english_certificate-3fe4825200e24ce98d386a9c26e2a65a.pdf` | (missing) |

### candidate_no = SH20271598

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=119` `application_id=1630` `exam_name=其他` `score_text=458` `certificate_attachment_url=/api/v1/portal/attachments/student-2897/english_certificate/english_certificate-1834fb9d580c43a99385988914060893.pdf` | (missing) |

### candidate_no = SH20271599

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1067` `application_id=1631` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1357/english_certificate/english_certificate-41c3acee33d24e3384774ed7f95cdc64.pdf` | (missing) |

### candidate_no = SH20271600

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=924` `application_id=1632` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1599/english_certificate/english_certificate-cc362502b41548df975b05a4ef7abc56.pdf` | (missing) |

### candidate_no = SH20271601

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1312` `application_id=1633` `exam_name=CET-6` `score_text=490` `certificate_attachment_url=/api/v1/portal/attachments/student-1005/english_certificate/english_certificate-2a013c161dfc47bb8f65610712a18a42.pdf` | (missing) |

### candidate_no = SH20271602

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=358` `application_id=1634` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2564/english_certificate/english_certificate-edda79da303247f79724e1a56fae1a94.pdf` | (missing) |

### candidate_no = SH20271603

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=130` `application_id=1635` `exam_name=CET-6` `score_text=454` `certificate_attachment_url=/api/v1/portal/attachments/student-2883/english_certificate/english_certificate-ef393426be1d414a8c50eb6aca038c6a.pdf` | (missing) |

### candidate_no = SH20271604

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=298` `application_id=1636` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2640/english_certificate/english_certificate-6e05882b61b947f2868a5a3630c53b25.pdf` | (missing) |

### candidate_no = SH20271605

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=154` `application_id=1637` `exam_name=CET-6` `score_text=442` `certificate_attachment_url=/api/v1/portal/attachments/student-2849/english_certificate/english_certificate-a2117525c46846d4bcb73cd4ee341472.pdf` | (missing) |

### candidate_no = SH20271606

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=532` `application_id=1638` `exam_name=CET-6` `score_text=559` `certificate_attachment_url=/api/v1/portal/attachments/student-2259/english_certificate/english_certificate-208c92fa13474fefaf921adb4a229d2e.pdf` | (missing) |

### candidate_no = SH20271607

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=83` `application_id=1639` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2952/english_certificate/english_certificate-1d4276423ce94080b06177a0853bf97f.pdf` | (missing) |

### candidate_no = SH20271608

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=899` `application_id=1640` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1648/english_certificate/english_certificate-4924c60fc8374763ab04969dca44fa0d.pdf` | (missing) |

### candidate_no = SH20271609

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=64` `application_id=1641` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2982/english_certificate/english_certificate-5d997fcacb004f85b3736b691932da2a.pdf` | (missing) |

### candidate_no = SH20271610

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1792` `application_id=1642` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-284/english_certificate/english_certificate-7d392688737149df90820bd832fbcd7a.pdf` | (missing) |

### candidate_no = SH20271611

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=63` `application_id=1643` `exam_name=CET-6` `score_text=597` `certificate_attachment_url=/api/v1/portal/attachments/student-2985/english_certificate/english_certificate-4e5eded4a0d24742a5956e57b39a583a.pdf` | (missing) |

### candidate_no = SH20271612

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=783` `application_id=1644` `exam_name=CET-6` `score_text=459` `certificate_attachment_url=/api/v1/portal/attachments/student-1843/english_certificate/english_certificate-5980aed033ab47b395ac3f0cd49ce9b6.pdf` | (missing) |

### candidate_no = SH20271613

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=133` `application_id=1645` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2879/english_certificate/english_certificate-04f5798876504510bf9aea957f3804aa.pdf` | (missing) |

### candidate_no = SH20271614

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=849` `application_id=1646` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1739/english_certificate/english_certificate-f830c7472f7d46209b2a2f02a427dff3.pdf` | (missing) |

### candidate_no = SH20271615

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=267` `application_id=1647` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2683/english_certificate/english_certificate-af2c2d52b27448b9a0250064da9e6f2d.pdf` | (missing) |

### candidate_no = SH20271616

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1472` `application_id=1648` `exam_name=其他` `score_text=四级507` `certificate_attachment_url=/api/v1/portal/attachments/student-788/english_certificate/english_certificate-6055df98c324418cb9afe71ed09dd719.pdf` | (missing) |

### candidate_no = SH20271617

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=458` `application_id=1649` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2372/english_certificate/english_certificate-64aec13b18ca4a9a9aaef34bb9bfdc33.pdf` | (missing) |

### candidate_no = SH20271618

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1563` `application_id=1650` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-643/english_certificate/english_certificate-2c6e151fba9245eeb547e04f2b1f3311.pdf` | (missing) |

### candidate_no = SH20271619

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=106` `application_id=1651` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2915/english_certificate/english_certificate-0f132ecb60794088b85cf101b4391d64.pdf` | (missing) |

### candidate_no = SH20271620

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=85` `application_id=1652` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2948/english_certificate/english_certificate-f46fb783b75f4278ba5ff96d492797f1.png` | (missing) |

### candidate_no = SH20271621

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=306` `application_id=1653` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2630/english_certificate/english_certificate-e6c57a3134b74399a8e69c39c16ec3ae.pdf` | (missing) |

### candidate_no = SH20271622

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=223` `application_id=1654` `exam_name=CET-6` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-2740/english_certificate/english_certificate-deec8aa9f581488eaf67e4ddec163b85.pdf` | (missing) |

### candidate_no = SH20271623

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=144` `application_id=1655` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2862/english_certificate/english_certificate-7e419e7e81e04949806ce89202bebc89.pdf` | (missing) |

### candidate_no = SH20271624

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1448` `application_id=1656` `exam_name=CET-6` `score_text=614` `certificate_attachment_url=/api/v1/portal/attachments/student-826/english_certificate/english_certificate-bfaa8c69eb7a4c11a1c0a58d67cacd6c.pdf` | (missing) |

### candidate_no = SH20271625

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1261` `application_id=1657` `exam_name=CET-6` `score_text=569` `certificate_attachment_url=/api/v1/portal/attachments/student-1068/english_certificate/english_certificate-881a9dfd58444a1c961e7ef755a29abe.pdf` | (missing) |
| 第 2 行 | `id=1262` `application_id=1657` `exam_name=其他` `score_text=592` `certificate_attachment_url=/api/v1/portal/attachments/student-1068/english_certificate/english_certificate-b514d00e069040e881279557f0ed23f6.pdf` | (missing) |

### candidate_no = SH20271626

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=821` `application_id=1658` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1795/english_certificate/english_certificate-9399ea6c282d470db7ee990339b27145.pdf` | (missing) |

### candidate_no = SH20271627

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=200` `application_id=1659` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2774/english_certificate/english_certificate-9c637d0902c04c3ab56494dec2fa347d.pdf` | (missing) |

### candidate_no = SH20271628

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=174` `application_id=1660` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2817/english_certificate/english_certificate-1953c0e0b0fc4dd8a092388b4c9a968f.pdf` | (missing) |

### candidate_no = SH20271629

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=143` `application_id=1661` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2864/english_certificate/english_certificate-3107ee82a0084f8ab30d6c9b8d896f99.pdf` | (missing) |

### candidate_no = SH20271630

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1682` `application_id=1662` `exam_name=CET-6` `score_text=532` `certificate_attachment_url=/api/v1/portal/attachments/student-471/english_certificate/english_certificate-8a25dfb5519b412e8e0d575efdc79f39.pdf` | (missing) |

### candidate_no = SH20271631

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=149` `application_id=1663` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2856/english_certificate/english_certificate-31b8c98b30554b9aa9d7fd576f00a5de.png` | (missing) |

### candidate_no = SH20271632

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=66` `application_id=1664` `exam_name=CET-6` `score_text=542` `certificate_attachment_url=/api/v1/portal/attachments/student-2979/english_certificate/english_certificate-454af3db0f794b3ca8c4e846c971c457.pdf` | (missing) |

### candidate_no = SH20271633

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=60` `application_id=1665` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2988/english_certificate/english_certificate-943fdb4a7ad548dfbb74c10c76fa84a5.pdf` | (missing) |

### candidate_no = SH20271634

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1242` `application_id=1666` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1092/english_certificate/english_certificate-70136d0f75ac48e59b37a7d24e8d3922.pdf` | (missing) |

### candidate_no = SH20271635

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1664` `application_id=1667` `exam_name=CET-6` `score_text=515` `certificate_attachment_url=/api/v1/portal/attachments/student-497/english_certificate/english_certificate-a32928edfebe4c4a8765802d2f44f5a6.pdf` | (missing) |
| 第 2 行 | `id=1665` `application_id=1667` `exam_name=其他` `score_text=604` `certificate_attachment_url=/api/v1/portal/attachments/student-497/english_certificate/english_certificate-a8e6a27031294ccc9dedbfe8d06876bb.pdf` | (missing) |

### candidate_no = SH20271636

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1730` `application_id=1668` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-398/english_certificate/english_certificate-b96d35816fc547bea0b8b69a02afffa7.pdf` | (missing) |

### candidate_no = SH20271637

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=941` `application_id=1669` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1575/english_certificate/english_certificate-267b903673894cd4864e4e20cd3fb634.pdf` | (missing) |

### candidate_no = SH20271638

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=667` `application_id=1670` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2044/english_certificate/english_certificate-f932bf0f403b4aba9afc7b48f3aadf2a.pdf` | (missing) |

### candidate_no = SH20271639

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1905` `application_id=1671` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-108/english_certificate/english_certificate-d9be5ddbee6c453aada47131e152941e.pdf` | (missing) |

### candidate_no = SH20271640

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1167` `application_id=1672` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1210/english_certificate/english_certificate-aa6342ce0c844639954b34163703d30b.pdf` | (missing) |

### candidate_no = SH20271641

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=454` `application_id=1673` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2379/english_certificate/english_certificate-3173b5fa8bbd409195efb9a578b02e2c.pdf` | (missing) |

### candidate_no = SH20271642

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=833` `application_id=1674` `exam_name=CET-6` `score_text=529` `certificate_attachment_url=/api/v1/portal/attachments/student-1767/english_certificate/english_certificate-b1db376713be4c83be2bb1198115a010.pdf` | (missing) |

### candidate_no = SH20271643

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=764` `application_id=1675` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1870/english_certificate/english_certificate-c9ec64c459d64046ad4e4ad42f6cc92a.pdf` | (missing) |

### candidate_no = SH20271644

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1254` `application_id=1676` `exam_name=CET-6` `score_text=551` `certificate_attachment_url=/api/v1/portal/attachments/student-1077/english_certificate/english_certificate-dba2fbf1ff4e40a4b7295f1992a1d488.pdf` | (missing) |

### candidate_no = SH20271645

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=615` `application_id=1677` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2130/english_certificate/english_certificate-de0e9eeaee044555971f9aa21cef40ea.pdf` | (missing) |

### candidate_no = SH20271646

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=57` `application_id=1678` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2994/english_certificate/english_certificate-10aaa3efd9d24359802ea7a775e40b7d.pdf` | (missing) |

### candidate_no = SH20271647

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=203` `application_id=1679` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2770/english_certificate/english_certificate-ac26e076f5d44df59f137d7c96b70d9b.jpg` | (missing) |

### candidate_no = SH20271648

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=703` `application_id=1680` `exam_name=其他` `score_text=浙江省笔译大赛二等奖` `certificate_attachment_url=/api/v1/portal/attachments/student-1972/english_certificate/english_certificate-93842df25718452cb9af071b2f23b5a6.pdf` | (missing) |
| 第 2 行 | `id=704` `application_id=1680` `exam_name=CET-6` `score_text=426` `certificate_attachment_url=/api/v1/portal/attachments/student-1972/english_certificate/english_certificate-ca3a02656731497b8c6562e61469a340.pdf` | (missing) |

### candidate_no = SH20271649

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=47` `application_id=1681` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3006/english_certificate/english_certificate-ff1f420b935947ddb1fb6887c355f152.pdf` | (missing) |

### candidate_no = SH20271650

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=90` `application_id=1682` `exam_name=CET-6` `score_text=443` `certificate_attachment_url=/api/v1/portal/attachments/student-2940/english_certificate/english_certificate-8ab719da91d2464c928ac3308a76450e.jpg` | (missing) |

### candidate_no = SH20271651

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=53` `application_id=1683` `exam_name=CET-6` `score_text=673` `certificate_attachment_url=/api/v1/portal/attachments/student-2998/english_certificate/english_certificate-65b7bab38a124741945c1865c0a27ac1.pdf` | (missing) |

### candidate_no = SH20271652

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=49` `application_id=1684` `exam_name=CET-6` `score_text=517` `certificate_attachment_url=/api/v1/portal/attachments/student-3004/english_certificate/english_certificate-cde05c14eca1433795263fca453ab21d.pdf` | (missing) |

### candidate_no = SH20271653

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1360` `application_id=1685` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-939/english_certificate/english_certificate-73b69246f68d4125b4517fefb93c4a77.pdf` | (missing) |

### candidate_no = SH20271654

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=733` `application_id=1686` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1922/english_certificate/english_certificate-ea732a1abfd741fcae41468db2356416.png` | (missing) |

### candidate_no = SH20271655

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=374` `application_id=1687` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2537/english_certificate/english_certificate-d0f099765f8e48d39ac480f6a9a3cb4c.png` | (missing) |

### candidate_no = SH20271656

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=784` `application_id=1688` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1842/english_certificate/english_certificate-fd05916d363a455a83a6b54f0f262eb1.pdf` | (missing) |

### candidate_no = SH20271657

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=832` `application_id=1689` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1772/english_certificate/english_certificate-715acf6a7fb2470dad6ace9fc45b8367.pdf` | (missing) |

### candidate_no = SH20271658

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=80` `application_id=1690` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2954/english_certificate/english_certificate-3d907a565f044b26a67f8a20f48c6b6f.pdf` | (missing) |

### candidate_no = SH20271659

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1396` `application_id=1691` `exam_name=CET-6` `score_text=556` `certificate_attachment_url=/api/v1/portal/attachments/student-888/english_certificate/english_certificate-2a9398d77584424682cf531d2fd7209e.pdf` | (missing) |

### candidate_no = SH20271660

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1348` `application_id=1692` `exam_name=CET-6` `score_text=586` `certificate_attachment_url=/api/v1/portal/attachments/student-958/english_certificate/english_certificate-b35bf991c00047f6a10df5de4ce7408e.pdf` | (missing) |

### candidate_no = SH20271661

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=299` `application_id=1693` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2639/english_certificate/english_certificate-b754400417fd47959474bd4c1e16acab.jpg` | (missing) |

### candidate_no = SH20271662

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=794` `application_id=1694` `exam_name=CET-6` `score_text=488` `certificate_attachment_url=/api/v1/portal/attachments/student-1830/english_certificate/english_certificate-ca5a7a8ae75246858804d301aada09a3.pdf` | (missing) |
| 第 2 行 | `id=795` `application_id=1694` `exam_name=其他` `score_text=552` `certificate_attachment_url=/api/v1/portal/attachments/student-1830/english_certificate/english_certificate-9fc023a09db245238282488e82dda0d2.pdf` | (missing) |

### candidate_no = SH20271663

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=75` `application_id=1695` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2960/english_certificate/english_certificate-14e3820ed3974d01abb3f9c7c25bc178.pdf` | (missing) |

### candidate_no = SH20271664

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=170` `application_id=1696` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2823/english_certificate/english_certificate-fc535f8cda0d4c66a1556b489f9f8eaa.pdf` | (missing) |

### candidate_no = SH20271665

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=731` `application_id=1697` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1926/english_certificate/english_certificate-bef2a3cc8b9e47e6834be4413f5a1bb5.pdf` | (missing) |

### candidate_no = SH20271666

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=46` `application_id=1698` `exam_name=CET-6` `score_text=504` `certificate_attachment_url=/api/v1/portal/attachments/student-3007/english_certificate/english_certificate-be567c16f5004dba9ebdfcfb8adc8407.pdf` | (missing) |

### candidate_no = SH20271667

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=41` `application_id=1699` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3015/english_certificate/english_certificate-f896e17fca094b89a742722f98b3217a.pdf` | (missing) |

### candidate_no = SH20271668

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=610` `application_id=1700` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2137/english_certificate/english_certificate-29d08d4bdbe44e7ba7e8f90d11a8e8a8.pdf` | (missing) |

### candidate_no = SH20271669

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=122` `application_id=1701` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2894/english_certificate/english_certificate-7b634efe135444a4a345495101ec5901.jpg` | (missing) |

### candidate_no = SH20271670

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=420` `application_id=1702` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2438/english_certificate/english_certificate-75855a8b549644a880e318286ae070c4.pdf` | (missing) |

### candidate_no = SH20271671

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=39` `application_id=1703` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3017/english_certificate/english_certificate-0e9b39bc37304d20a6838f82724cd635.pdf` | (missing) |

### candidate_no = SH20271672

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=232` `application_id=1704` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2731/english_certificate/english_certificate-9e49b74ab2824b3e97fdfc1dde94eed0.png` | (missing) |

### candidate_no = SH20271673

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=87` `application_id=1705` `exam_name=CET-6` `score_text=531` `certificate_attachment_url=/api/v1/portal/attachments/student-2945/english_certificate/english_certificate-beac010af6284aeb978e7a65aac878a8.pdf` | (missing) |

### candidate_no = SH20271674

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=874` `application_id=1706` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1701/english_certificate/english_certificate-e2634dc130344794b5044fcc3e386363.pdf` | (missing) |

### candidate_no = SH20271675

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=906` `application_id=1707` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1634/english_certificate/english_certificate-6d082a9a4d7643f7aadb1d1c192f64ce.pdf` | (missing) |

### candidate_no = SH20271676

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=370` `application_id=1708` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2542/english_certificate/english_certificate-26e04745f3d04313a3443665101f743c.pdf` | (missing) |

### candidate_no = SH20271677

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=959` `application_id=1709` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-1538/english_certificate/english_certificate-ebb15beba2484ee88c84a4c016c6a58d.pdf` | (missing) |
| 第 2 行 | `id=960` `application_id=1709` `exam_name=CET-6` `score_text=609` `certificate_attachment_url=/api/v1/portal/attachments/student-1538/english_certificate/english_certificate-9951f4f54a9348a8a0233b339dc6d3fa.pdf` | (missing) |

### candidate_no = SH20271678

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1155` `application_id=1710` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1229/english_certificate/english_certificate-dd92497440074ed498377cd2c7de7d52.pdf` | (missing) |

### candidate_no = SH20271679

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=813` `application_id=1711` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1809/english_certificate/english_certificate-1c2ad13c2f6441f8be7ca004f0eb3ee9.pdf` | (missing) |

### candidate_no = SH20271680

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=205` `application_id=1712` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2767/english_certificate/english_certificate-8581e1de642948afb5fadc2015a58952.pdf` | (missing) |

### candidate_no = SH20271681

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=113` `application_id=1713` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2904/english_certificate/english_certificate-72a25b0576dc463f804171eedbcd00e7.pdf` | (missing) |

### candidate_no = SH20271682

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1884` `application_id=1714` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-139/english_certificate/english_certificate-051106528c8f4d64bdb42213036b2483.pdf` | (missing) |

### candidate_no = SH20271683

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=212` `application_id=1715` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2758/english_certificate/english_certificate-1c757eecaf554ddda8f133c038149695.jpg` | (missing) |

### candidate_no = SH20271684

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=958` `application_id=1716` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1539/english_certificate/english_certificate-4e0783519a294920af624bfc0c79c5c9.pdf` | (missing) |

### candidate_no = SH20271685

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=513` `application_id=1717` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2283/english_certificate/english_certificate-1bc92ee717bd457abbe152d1f892842a.pdf` | (missing) |

### candidate_no = SH20271686

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=588` `application_id=1718` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2173/english_certificate/english_certificate-334cd2e881364fe9b4e0e66cba395f62.pdf` | (missing) |

### candidate_no = SH20271687

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1116` `application_id=1719` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1287/english_certificate/english_certificate-da6a2db796554c328214be7b5c914463.pdf` | (missing) |

### candidate_no = SH20271688

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=403` `application_id=1720` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2480/english_certificate/english_certificate-479efd8e1ba745f9ae931ec57b329bdc.pdf` | (missing) |

### candidate_no = SH20271689

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=35` `application_id=1721` `exam_name=CET-6` `score_text=552` `certificate_attachment_url=/api/v1/portal/attachments/student-3021/english_certificate/english_certificate-f4256ce83f2146098e6f5db5e90753de.pdf` | (missing) |

### candidate_no = SH20271690

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1365` `application_id=1722` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-935/english_certificate/english_certificate-2246bb57c59943c89586db0482a61eac.pdf` | (missing) |

### candidate_no = SH20271691

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1172` `application_id=1723` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1204/english_certificate/english_certificate-c1b6be8eb58042cdb458b1468d5fec74.pdf` | (missing) |

### candidate_no = SH20271692

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=815` `application_id=1724` `exam_name=CET-6` `score_text=449` `certificate_attachment_url=/api/v1/portal/attachments/student-1806/english_certificate/english_certificate-34c18aa2bc234a0ab8ef9a399e8d30ef.pdf` | (missing) |

### candidate_no = SH20271693

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=630` `application_id=1725` `exam_name=CET-6` `score_text=585` `certificate_attachment_url=/api/v1/portal/attachments/student-2098/english_certificate/english_certificate-8e39b321043a4acdadbdd61b43c0e85a.pdf` | (missing) |

### candidate_no = SH20271694

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=409` `application_id=1726` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2465/english_certificate/english_certificate-7cc1319e8c8740a18489a9d516546d6d.pdf` | (missing) |

### candidate_no = SH20271695

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=442` `application_id=1727` `exam_name=CET-6` `score_text=511` `certificate_attachment_url=/api/v1/portal/attachments/student-2393/english_certificate/english_certificate-c70dedb6071c467290a9a632a0ed5d9b.pdf` | (missing) |

### candidate_no = SH20271696

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=172` `application_id=1728` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2821/english_certificate/english_certificate-82ef9d28fb5541d89521296474e7594a.pdf` | (missing) |

### candidate_no = SH20271697

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1764` `application_id=1729` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-335/english_certificate/english_certificate-d8450c6de6e9469484adf4ce325c944a.pdf` | (missing) |

### candidate_no = SH20271698

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=58` `application_id=1730` `exam_name=CET-6` `score_text=487` `certificate_attachment_url=/api/v1/portal/attachments/student-2992/english_certificate/english_certificate-f2dc947b8d2d4c7fb2617edb75a912ba.pdf` | (missing) |

### candidate_no = SH20271699

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1038` `application_id=1731` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1410/english_certificate/english_certificate-29544d28094a42a589652b8d917ece29.pdf` | (missing) |

### candidate_no = SH20271700

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=705` `application_id=1732` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1971/english_certificate/english_certificate-7afd17ee6592493c82d41877851a2d0e.pdf` | (missing) |

### candidate_no = SH20271701

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=431` `application_id=1733` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2409/english_certificate/english_certificate-ee9d4ef2cdf840889327ecb3b163a333.pdf` | (missing) |

### candidate_no = SH20271702

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=868` `application_id=1734` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1708/english_certificate/english_certificate-ea48feb96d394090ba7b66e8f829caab.jpg` | (missing) |

### candidate_no = SH20271703

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=489` `application_id=1735` `exam_name=CET-6` `score_text=606` `certificate_attachment_url=/api/v1/portal/attachments/student-2323/english_certificate/english_certificate-3586675d173d4cb0892059c85eacbf80.pdf` | (missing) |

### candidate_no = SH20271704

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=155` `application_id=1736` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2847/english_certificate/english_certificate-cbda8a68e7004bf2b73667da6ccced5b.pdf` | (missing) |

### candidate_no = SH20271705

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=45` `application_id=1737` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-3008/english_certificate/english_certificate-ac6a14422f4d4f9695775cc39f6fbb33.jpg` | (missing) |

### candidate_no = SH20271706

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=433` `application_id=1738` `exam_name=CET-6` `score_text=532` `certificate_attachment_url=/api/v1/portal/attachments/student-2407/english_certificate/english_certificate-7db93e4e81a24782bf94dff4e10b6138.pdf` | (missing) |

### candidate_no = SH20271707

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=34` `application_id=1739` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3022/english_certificate/english_certificate-e85d0e34c8ab405c9f79b0c4abc94f80.pdf` | (missing) |

### candidate_no = SH20271708

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=88` `application_id=1740` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2943/english_certificate/english_certificate-87c23d27ad4c4d17881dd53fcb3d20fb.pdf` | (missing) |

### candidate_no = SH20271709

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1118` `application_id=1741` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1284/english_certificate/english_certificate-1ced4b28ca0f43c8b942e8f148a8c124.pdf` | (missing) |

### candidate_no = SH20271710

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1861` `application_id=1742` `exam_name=CET-6` `score_text=459` `certificate_attachment_url=/api/v1/portal/attachments/student-169/english_certificate/english_certificate-fd725048b0b7488a9d49cd3e24808709.pdf` | (missing) |

### candidate_no = SH20271711

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=575` `application_id=1743` `exam_name=CET-6` `score_text=602` `certificate_attachment_url=/api/v1/portal/attachments/student-2192/english_certificate/english_certificate-477d794512914a3a940ac4b7a3f5c6c5.pdf` | (missing) |

### candidate_no = SH20271712

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=28` `application_id=1744` `exam_name=CET-6` `score_text=498` `certificate_attachment_url=/api/v1/portal/attachments/student-3030/english_certificate/english_certificate-0e9475d121bd46d2a92ae33dc20373bc.pdf` | (missing) |

### candidate_no = SH20271713

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1233` `application_id=1745` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1109/english_certificate/english_certificate-cf806705747d468ba2a602963c471ff1.pdf` | (missing) |

### candidate_no = SH20271714

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=235` `application_id=1746` `exam_name=CET-6` `score_text=464` `certificate_attachment_url=/api/v1/portal/attachments/student-2728/english_certificate/english_certificate-e43227f140c24326b0f24dfdf050a482.pdf` | (missing) |

### candidate_no = SH20271715

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=297` `application_id=1747` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2641/english_certificate/english_certificate-e8faf444fa054596b386702c9bf273b4.pdf` | (missing) |

### candidate_no = SH20271716

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=417` `application_id=1748` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2449/english_certificate/english_certificate-d288aa0c8dff4cbc829e484d61d9ff5b.pdf` | (missing) |

### candidate_no = SH20271717

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=162` `application_id=1749` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2837/english_certificate/english_certificate-115ba2ccb81740c494d50ea544970ea6.pdf` | (missing) |

### candidate_no = SH20271718

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=56` `application_id=1750` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2995/english_certificate/english_certificate-051b26423f2c4587932189cab544d74a.pdf` | (missing) |

### candidate_no = SH20271719

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=156` `application_id=1751` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2845/english_certificate/english_certificate-3a79961864414affa343ca59a3f71b9d.pdf` | (missing) |

### candidate_no = SH20271720

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=140` `application_id=1752` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2868/english_certificate/english_certificate-ab8afab7affd4ee08e6c06b4e8652749.pdf` | (missing) |

### candidate_no = SH20271721

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=104` `application_id=1753` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2918/english_certificate/english_certificate-c67fd304adee4974b70bc7dc58a12301.pdf` | (missing) |

### candidate_no = SH20271722

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1336` `application_id=1754` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-973/english_certificate/english_certificate-1ebf2130cd8044d48d092903e08e9a1f.pdf` | (missing) |

### candidate_no = SH20271723

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=529` `application_id=1755` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2262/english_certificate/english_certificate-d9442cf4f3b14e1fbcf47398952b93f7.pdf` | (missing) |

### candidate_no = SH20271724

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=434` `application_id=1756` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2406/english_certificate/english_certificate-b82b8e5ffaeb4971b379f9e2f3694102.pdf` | (missing) |

### candidate_no = SH20271725

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=418` `application_id=1757` `exam_name=CET-6` `score_text=566` `certificate_attachment_url=/api/v1/portal/attachments/student-2442/english_certificate/english_certificate-2a6206b29ec04b7e81a7d6c7f05cd2a2.pdf` | (missing) |

### candidate_no = SH20271726

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1120` `application_id=1758` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1282/english_certificate/english_certificate-62b8ac3fb9c44d6dae42d0e296ab5b58.pdf` | (missing) |

### candidate_no = SH20271727

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=40` `application_id=1759` `exam_name=CET-6` `score_text=514` `certificate_attachment_url=/api/v1/portal/attachments/student-3016/english_certificate/english_certificate-452f413b966442529e4e9331e98ae134.pdf` | (missing) |

### candidate_no = SH20271728

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=898` `application_id=1760` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1649/english_certificate/english_certificate-4870799adecf4c43921e82aa81cb9b9b.pdf` | (missing) |

### candidate_no = SH20271729

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=38` `application_id=1761` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3018/english_certificate/english_certificate-f8d9c55a6ae348ed90f63b7dfc2bb09a.pdf` | (missing) |

### candidate_no = SH20271730

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=346` `application_id=1762` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2579/english_certificate/english_certificate-1aad7bed7e7c4853beaa7da8a57ff18b.pdf` | (missing) |

### candidate_no = SH20271731

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=42` `application_id=1763` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3012/english_certificate/english_certificate-abdb54f13b704c84bc2f6e5f8cf792f4.pdf` | (missing) |

### candidate_no = SH20271732

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=991` `application_id=1764` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1488/english_certificate/english_certificate-a2df3725f8084be6911a167e2712f872.pdf` | (missing) |

### candidate_no = SH20271733

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1210` `application_id=1765` `exam_name=CET-6` `score_text=495` `certificate_attachment_url=/api/v1/portal/attachments/student-1136/english_certificate/english_certificate-e1b78a8d0b68466eb2268834229bbed1.pdf` | (missing) |

### candidate_no = SH20271734

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=303` `application_id=1766` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2635/english_certificate/english_certificate-1515ac8dbbc149c19b435e5984eb469a.pdf` | (missing) |

### candidate_no = SH20271735

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=51` `application_id=1767` `exam_name=CET-6` `score_text=511` `certificate_attachment_url=/api/v1/portal/attachments/student-3001/english_certificate/english_certificate-c6df40c0058c46b8a1f2567e070f3c47.pdf` | (missing) |

### candidate_no = SH20271736

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1608` `application_id=1768` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-579/english_certificate/english_certificate-09e5c63af861410cb8b8037900403190.pdf` | (missing) |

### candidate_no = SH20271737

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1955` `application_id=1769` `exam_name=CET-6` `score_text=585` `certificate_attachment_url=/api/v1/portal/attachments/student-42/english_certificate/english_certificate-79d27d6b464e40acbc2e4b4428adf56b.pdf` | (missing) |

### candidate_no = SH20271738

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=550` `application_id=1770` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2235/english_certificate/english_certificate-f8bf78829fa343ebb7925077cbefbf18.pdf` | (missing) |

### candidate_no = SH20271739

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=534` `application_id=1771` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2254/english_certificate/english_certificate-e798f363be2346bfbded6fd88afa5ed3.pdf` | (missing) |

### candidate_no = SH20271740

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1522` `application_id=1772` `exam_name=CET-6` `score_text=477` `certificate_attachment_url=/api/v1/portal/attachments/student-709/english_certificate/english_certificate-5c8ab9915f304dd686c51d928315c34b.pdf` | (missing) |

### candidate_no = SH20271741

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1540` `application_id=1773` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-682/english_certificate/english_certificate-604057944cf14aaca06edfd6aa14b453.pdf` | (missing) |

### candidate_no = SH20271742

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=21` `application_id=1774` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3039/english_certificate/english_certificate-205060e844ba487caa7c752f81269fd0.pdf` | (missing) |

### candidate_no = SH20271743

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=65` `application_id=1775` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2981/english_certificate/english_certificate-15714626df414b6a8c8cf17d0cee27ad.pdf` | (missing) |

### candidate_no = SH20271744

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=120` `application_id=1776` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2896/english_certificate/english_certificate-e152e755efca4613975aff5bad3b4c19.pdf` | (missing) |

### candidate_no = SH20271745

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=31` `application_id=1777` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3026/english_certificate/english_certificate-c61c1c3125064ab8b825e89211a11a5b.pdf` | (missing) |

### candidate_no = SH20271746

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1121` `application_id=1778` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1281/english_certificate/english_certificate-0c64bd6b7d2944698a44dc397ba292f1.pdf` | (missing) |

### candidate_no = SH20271747

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=209` `application_id=1779` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2762/english_certificate/english_certificate-b55b9082a1834e499aebded9fcb22266.pdf` | (missing) |

### candidate_no = SH20271748

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=746` `application_id=1780` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1898/english_certificate/english_certificate-3b8ffa1b003c4d0ea9de2e472c5d1251.pdf` | (missing) |

### candidate_no = SH20271749

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1983` `application_id=1781` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2917/english_certificate/english_certificate-c222375fffdc42c7bef0659d741a3b2d.pdf` | (missing) |

### candidate_no = SH20271750

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=501` `application_id=1782` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2302/english_certificate/english_certificate-45d0759a7dd14bfb82403704323ce3c6.pdf` | (missing) |

### candidate_no = SH20271751

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=136` `application_id=1783` `exam_name=其他` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2873/english_certificate/english_certificate-69adcf33dde042b6852454107e3b9bd7.pdf` | (missing) |

### candidate_no = SH20271752

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=24` `application_id=1784` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3035/english_certificate/english_certificate-07037f8cb7f2441fb727a2c711b63933.pdf` | (missing) |

### candidate_no = SH20271753

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=26` `application_id=1785` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3033/english_certificate/english_certificate-f86e7d59ed08403c90de2f3696d90cb3.pdf` | (missing) |

### candidate_no = SH20271754

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=423` `application_id=1786` `exam_name=CET-6` `score_text=508` `certificate_attachment_url=/api/v1/portal/attachments/student-2431/english_certificate/english_certificate-92bc41a7420040c0bd444c3f4445d6dd.pdf` | (missing) |

### candidate_no = SH20271755

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=37` `application_id=1787` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3019/english_certificate/english_certificate-2285887d37384183a070adabf00ed886.pdf` | (missing) |

### candidate_no = SH20271756

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=36` `application_id=1788` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3020/english_certificate/english_certificate-2386f05da4c343668acf7c5d1b63ab23.pdf` | (missing) |

### candidate_no = SH20271757

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=168` `application_id=1789` `exam_name=CET-6` `score_text=478` `certificate_attachment_url=/api/v1/portal/attachments/student-2827/english_certificate/english_certificate-5ebc1121f8ec4d05a522e2b0ad9e9393.pdf` | (missing) |

### candidate_no = SH20271758

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=23` `application_id=1790` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3036/english_certificate/english_certificate-e243de95fe7243d3a4118eb5bec7c6d1.pdf` | (missing) |

### candidate_no = SH20271759

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1245` `application_id=1791` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1089/english_certificate/english_certificate-facc153646874484a95196df6ac219d4.pdf` | (missing) |

### candidate_no = SH20271760

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=110` `application_id=1792` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2907/english_certificate/english_certificate-19c7491c40be47aaa8cae5bd04f353be.pdf` | (missing) |

### candidate_no = SH20271761

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=587` `application_id=1793` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2174/english_certificate/english_certificate-fd2dd9ab49b54776ae4cc654e4df3f44.jpg` | (missing) |

### candidate_no = SH20271762

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=204` `application_id=1794` `exam_name=其他` `score_text=442` `certificate_attachment_url=/api/v1/portal/attachments/student-2768/english_certificate/english_certificate-819a24744d164d58867032712feb0a52.jpg` | (missing) |

### candidate_no = SH20271763

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1927` `application_id=1795` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-80/english_certificate/english_certificate-73df7cd4fbb4472285377fbc699d5a76.pdf` | (missing) |

### candidate_no = SH20271764

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1308` `application_id=1796` `exam_name=CET-6` `score_text=549` `certificate_attachment_url=/api/v1/portal/attachments/student-1011/english_certificate/english_certificate-d6f9e275576a45e68f5ba7163cc3ad13.pdf` | (missing) |

### candidate_no = SH20271765

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1001` `application_id=1797` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1470/english_certificate/english_certificate-529c185631d04d898af2bc9f67a30f0c.pdf` | (missing) |

### candidate_no = SH20271766

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=749` `application_id=1798` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1892/english_certificate/english_certificate-373e56130b1f4b3e8961e2faaa992e1f.pdf` | (missing) |

### candidate_no = SH20271767

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=182` `application_id=1799` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2799/english_certificate/english_certificate-58fab47c343747f89a70a231fb1078af.pdf` | (missing) |

### candidate_no = SH20271768

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1264` `application_id=1800` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1066/english_certificate/english_certificate-5e9ccccf9df94462ad0154a4f9b43a4e.pdf` | (missing) |

### candidate_no = SH20271769

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=644` `application_id=1801` `exam_name=CET-6` `score_text=550` `certificate_attachment_url=/api/v1/portal/attachments/student-2075/english_certificate/english_certificate-989978e7e5d4404c8b451b197b8ab8f4.pdf` | (missing) |
| 第 2 行 | `id=645` `application_id=1801` `exam_name=IELTS` `score_text=6.5` `certificate_attachment_url=/api/v1/portal/attachments/student-2075/english_certificate/english_certificate-48862549140048ae8388b036535876f9.pdf` | (missing) |

### candidate_no = SH20271770

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=181` `application_id=1802` `exam_name=CET-6` `score_text=512` `certificate_attachment_url=/api/v1/portal/attachments/student-2800/english_certificate/english_certificate-f98bd57ec104415b93e76f4b8092bdb5.jpg` | (missing) |

### candidate_no = SH20271771

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=153` `application_id=1803` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2851/english_certificate/english_certificate-277a160fae484be5aec6f5a3daa0957f.pdf` | (missing) |

### candidate_no = SH20271772

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=367` `application_id=1804` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2546/english_certificate/english_certificate-fb64acc85d1f4992b62f8d2aa7c084b9.pdf` | (missing) |

### candidate_no = SH20271773

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=248` `application_id=1805` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2709/english_certificate/english_certificate-9dc41766cfe84e0cb490a74e8d79a94c.pdf` | (missing) |

### candidate_no = SH20271774

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=72` `application_id=1806` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2967/english_certificate/english_certificate-bc983b003a51467aad263ea6adbd5fe2.pdf` | (missing) |

### candidate_no = SH20271775

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=89` `application_id=1807` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2942/english_certificate/english_certificate-022ab62f17c843359a4c4a504f4d2fc0.pdf` | (missing) |

### candidate_no = SH20271776

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=344` `application_id=1808` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2581/english_certificate/english_certificate-6ea39f01cbcd42b3a8cac4e053311e85.jpg` | (missing) |

### candidate_no = SH20271777

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=718` `application_id=1809` `exam_name=CET-6` `score_text=475` `certificate_attachment_url=/api/v1/portal/attachments/student-1947/english_certificate/english_certificate-dbdb25161a154a5e933d6f6f4a21cb8e.pdf` | (missing) |

### candidate_no = SH20271778

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=14` `application_id=1810` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3050/english_certificate/english_certificate-fc535f5fdaba47028861f440666cfdad.pdf` | (missing) |

### candidate_no = SH20271779

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=151` `application_id=1811` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2853/english_certificate/english_certificate-5a4d2635133e45399efc6439192f0330.pdf` | (missing) |

### candidate_no = SH20271780

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=52` `application_id=1812` `exam_name=CET-6` `score_text=534` `certificate_attachment_url=/api/v1/portal/attachments/student-2999/english_certificate/english_certificate-1928b23f4f1c44c8814e97181affc8d2.pdf` | (missing) |

### candidate_no = SH20271781

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=70` `application_id=1813` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2972/english_certificate/english_certificate-eaba1dde675f41d0aa24c583397cb274.pdf` | (missing) |

### candidate_no = SH20271782

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1143` `application_id=1814` `exam_name=CET-6` `score_text=458` `certificate_attachment_url=/api/v1/portal/attachments/student-1250/english_certificate/english_certificate-0abd215d7bd8402a8e5bf8d811f76f91.jpg` | (missing) |

### candidate_no = SH20271783

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=150` `application_id=1815` `exam_name=IELTS` `score_text=7.5` `certificate_attachment_url=/api/v1/portal/attachments/student-2854/english_certificate/english_certificate-f7555adcf4254b18b6ff3d64d4446bb1.pdf` | (missing) |

### candidate_no = SH20271784

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=17` `application_id=1816` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3045/english_certificate/english_certificate-a6fe34729a9546d7968fe59de32870d8.pdf` | (missing) |

### candidate_no = SH20271785

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1543` `application_id=1817` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-678/english_certificate/english_certificate-f4f7e2aa0866417e83912a056c7b34b9.jpg` | (missing) |

### candidate_no = SH20271786

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=836` `application_id=1818` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1764/english_certificate/english_certificate-ebe2ef65e7d84dbfa630c3aadaf1c16d.png` | (missing) |

### candidate_no = SH20271787

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=948` `application_id=1819` `exam_name=CET-6` `score_text=460` `certificate_attachment_url=/api/v1/portal/attachments/student-1557/english_certificate/english_certificate-e68dd7cb431e485bb4e5c7ac2a6da017.pdf` | (missing) |

### candidate_no = SH20271788

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=171` `application_id=1820` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2822/english_certificate/english_certificate-6f4d9aa182744e6db3e18d5e261807f2.pdf` | (missing) |

### candidate_no = SH20271789

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=494` `application_id=1821` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2313/english_certificate/english_certificate-7958e36aba7143bbbf78e8d6074b4dc2.pdf` | (missing) |

### candidate_no = SH20271790

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=526` `application_id=1822` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2265/english_certificate/english_certificate-3367ce5a44394ff2ad8e9257f8d902ba.pdf` | (missing) |

### candidate_no = SH20271791

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1161` `application_id=1823` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1218/english_certificate/english_certificate-ea1161fa90094706b5db6b357554beba.pdf` | (missing) |

### candidate_no = SH20271792

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1158` `application_id=1824` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1223/english_certificate/english_certificate-b6ce39b323e747bcafe4cf8bb70f3f17.pdf` | (missing) |

### candidate_no = SH20271793

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=95` `application_id=1825` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2933/english_certificate/english_certificate-b5270f765f6242e9a834ce1831de1e8a.pdf` | (missing) |

### candidate_no = SH20271794

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=69` `application_id=1826` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2973/english_certificate/english_certificate-27b4135aba4b49c19321ed5dce4b0563.jpg` | (missing) |

### candidate_no = SH20271795

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1257` `application_id=1827` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1073/english_certificate/english_certificate-e56636cbffb34a63b2d197d40fd49844.pdf` | (missing) |

### candidate_no = SH20271796

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=751` `application_id=1828` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1890/english_certificate/english_certificate-773bec8d989c41f9bc09a96884b7e6a5.pdf` | (missing) |

### candidate_no = SH20271797

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1129` `application_id=1829` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1270/english_certificate/english_certificate-eeb89757e6db494dad3752e2e701c640.pdf` | (missing) |

### candidate_no = SH20271798

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=246` `application_id=1830` `exam_name=CET-6` `score_text=494` `certificate_attachment_url=/api/v1/portal/attachments/student-2711/english_certificate/english_certificate-828da88edcdf47f0a1d580a59ee40184.jpg` | (missing) |

### candidate_no = SH20271799

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=91` `application_id=1831` `exam_name=CET-6` `score_text=464` `certificate_attachment_url=/api/v1/portal/attachments/student-2938/english_certificate/english_certificate-c73f56a7e0304c6d9445d87385227d1c.pdf` | (missing) |

### candidate_no = SH20271800

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=392` `application_id=1832` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2498/english_certificate/english_certificate-91883b6b65054baea23224a5f85e2a08.pdf` | (missing) |

### candidate_no = SH20271801

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1286` `application_id=1833` `exam_name=CET-6` `score_text=508` `certificate_attachment_url=/api/v1/portal/attachments/student-1041/english_certificate/english_certificate-bcc203a5eda248f5bf209198dbe49316.pdf` | (missing) |

### candidate_no = SH20271802

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=724` `application_id=1834` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1936/english_certificate/english_certificate-c1c5a2a7660f4100a54269d72d6795c8.jpg` | (missing) |

### candidate_no = SH20271803

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=548` `application_id=1835` `exam_name=CET-6` `score_text=520` `certificate_attachment_url=/api/v1/portal/attachments/student-2237/english_certificate/english_certificate-aaaf2650f70a4e65a00591c8dcd95b2a.pdf` | (missing) |

### candidate_no = SH20271804

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1549` `application_id=1836` `exam_name=CET-6` `score_text=563` `certificate_attachment_url=/api/v1/portal/attachments/student-669/english_certificate/english_certificate-09148308b26343518062881273db8172.pdf` | (missing) |

### candidate_no = SH20271805

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=44` `application_id=1837` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3010/english_certificate/english_certificate-130f9b286d9548d291b43202171818c0.pdf` | (missing) |

### candidate_no = SH20271806

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1232` `application_id=1838` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1111/english_certificate/english_certificate-8daab16e421144c9a2acfd26e5e1b796.pdf` | (missing) |

### candidate_no = SH20271807

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1389` `application_id=1839` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-896/english_certificate/english_certificate-2e0e1c1ff2054e7f9bfb476420bb4bbd.pdf` | (missing) |

### candidate_no = SH20271808

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=185` `application_id=1840` `exam_name=CET-6` `score_text=462` `certificate_attachment_url=/api/v1/portal/attachments/student-2796/english_certificate/english_certificate-59f91466379e43b697e67b84de314647.pdf` | (missing) |

### candidate_no = SH20271809

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1765` `application_id=1841` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-334/english_certificate/english_certificate-964176f6bfe4414aa753593a7e8a7942.pdf` | (missing) |

### candidate_no = SH20271810

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1848` `application_id=1842` `exam_name=CET-6` `score_text=456` `certificate_attachment_url=/api/v1/portal/attachments/student-190/english_certificate/english_certificate-6cf00c30d5f945aebdad1aa239a5d7e8.pdf` | (missing) |

### candidate_no = SH20271811

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=15` `application_id=1843` `exam_name=CET-6` `score_text=455` `certificate_attachment_url=/api/v1/portal/attachments/student-3047/english_certificate/english_certificate-c4102c066d2842e0b256a47cdd4a9a84.pdf` | (missing) |

### candidate_no = SH20271812

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=245` `application_id=1844` `exam_name=CET-6` `score_text=463` `certificate_attachment_url=/api/v1/portal/attachments/student-2712/english_certificate/english_certificate-12719f13b8bb4708bb5a584ba2ebd568.pdf` | (missing) |

### candidate_no = SH20271813

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=597` `application_id=1845` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2152/english_certificate/english_certificate-c6ed873ec7b940668a76719069cf9c88.pdf` | (missing) |

### candidate_no = SH20271814

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=361` `application_id=1846` `exam_name=CET-6` `score_text=459` `certificate_attachment_url=/api/v1/portal/attachments/student-2560/english_certificate/english_certificate-d2d6303766544df6aeba51ce57e04617.pdf` | (missing) |

### candidate_no = SH20271815

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=995` `application_id=1847` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1476/english_certificate/english_certificate-1aec1c4702564b5f895f5452cbd9a007.pdf` | (missing) |

### candidate_no = SH20271816

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=214` `application_id=1848` `exam_name=其他` `score_text=500` `certificate_attachment_url=/api/v1/portal/attachments/student-2756/english_certificate/english_certificate-8edc77810aa24326b88b2b9bfe85ddbe.pdf` | (missing) |

### candidate_no = SH20271817

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=781` `application_id=1849` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1845/english_certificate/english_certificate-1dc86cc4513446829dde5e1a1501ce9b.jpg` | (missing) |

### candidate_no = SH20271818

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=146` `application_id=1850` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2860/english_certificate/english_certificate-4601f77963834c98955bbf1a5779710d.jpg` | (missing) |

### candidate_no = SH20271819

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=231` `application_id=1851` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2732/english_certificate/english_certificate-f336b6a218fc4075a4a719c9f1e3cc40.pdf` | (missing) |

### candidate_no = SH20271820

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=913` `application_id=1852` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1617/english_certificate/english_certificate-76623011e338478c958d08ca135467c3.pdf` | (missing) |

### candidate_no = SH20271821

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=961` `application_id=1853` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1537/english_certificate/english_certificate-c34a4a1d00eb46289ebaa53fdac5cb52.pdf` | (missing) |

### candidate_no = SH20271822

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=116` `application_id=1854` `exam_name=CET-6` `score_text=518` `certificate_attachment_url=/api/v1/portal/attachments/student-2901/english_certificate/english_certificate-e2be449883f646db923329927076a3b0.png` | (missing) |

### candidate_no = SH20271823

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1310` `application_id=1855` `exam_name=CET-6` `score_text=563` `certificate_attachment_url=/api/v1/portal/attachments/student-1009/english_certificate/english_certificate-92587917f6d6450e8bb63152028d4043.pdf` | (missing) |

### candidate_no = SH20271824

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=801` `application_id=1856` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1822/english_certificate/english_certificate-cd267ed57d7f454786295e997d33bc45.pdf` | (missing) |

### candidate_no = SH20271825

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=450` `application_id=1857` `exam_name=CET-6` `score_text=543` `certificate_attachment_url=/api/v1/portal/attachments/student-2384/english_certificate/english_certificate-8334cee752314bf5b6615e7522ffd3cd.pdf` | (missing) |

### candidate_no = SH20271826

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=592` `application_id=1858` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2166/english_certificate/english_certificate-5494ffc15ffc43378ee3d0eb794f089a.jpg` | (missing) |

### candidate_no = SH20271827

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=16` `application_id=1859` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3046/english_certificate/english_certificate-a144f196e38e4d69a576e21a189fd0e5.jpg` | (missing) |

### candidate_no = SH20271828

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=414` `application_id=1860` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2455/english_certificate/english_certificate-ea954b9aa6664aceba8b47f0b847beab.pdf` | (missing) |

### candidate_no = SH20271829

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1468` `application_id=1861` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-792/english_certificate/english_certificate-81f0b1d3351e4bfab4d831d41d73dd89.pdf` | (missing) |

### candidate_no = SH20271830

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=27` `application_id=1862` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3032/english_certificate/english_certificate-8de88bb809aa40e0a615b8e620f049ba.jpg` | (missing) |

### candidate_no = SH20271831

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=471` `application_id=1863` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2353/english_certificate/english_certificate-ccf82519683a4e82974709f5679eb805.pdf` | (missing) |

### candidate_no = SH20271832

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=55` `application_id=1864` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2996/english_certificate/english_certificate-ad86e25bc79c40a599c5e01da7d9b873.pdf` | (missing) |

### candidate_no = SH20271833

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=353` `application_id=1865` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2570/english_certificate/english_certificate-348f3c44eb144ed2a7c0cbe4f589b089.pdf` | (missing) |

### candidate_no = SH20271834

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=502` `application_id=1866` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2301/english_certificate/english_certificate-7956e91b2eee48959494c501b904cf4d.pdf` | (missing) |

### candidate_no = SH20271835

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=18` `application_id=1867` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3044/english_certificate/english_certificate-63c0151c07ff4dd2a219e024fa8d7855.pdf` | (missing) |

### candidate_no = SH20271836

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=13` `application_id=1868` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3053/english_certificate/english_certificate-1c5b6ffc5d86472dba9d158c2cde2bf2.pdf` | (missing) |

### candidate_no = SH20271837

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=381` `application_id=1869` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2524/english_certificate/english_certificate-c4ff20eb6e5f40e99edd02f224300259.pdf` | (missing) |

### candidate_no = SH20271838

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=390` `application_id=1870` `exam_name=CET-6` `score_text=481` `certificate_attachment_url=/api/v1/portal/attachments/student-2501/english_certificate/english_certificate-92467cb4926145eaa6e45d2a7b6e941f.pdf` | (missing) |

### candidate_no = SH20271839

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=935` `application_id=1871` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1582/english_certificate/english_certificate-1f5091f4178e4db0a5812016a49c3785.pdf` | (missing) |

### candidate_no = SH20271840

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=777` `application_id=1872` `exam_name=CET-6` `score_text=443` `certificate_attachment_url=/api/v1/portal/attachments/student-1851/english_certificate/english_certificate-9dfc9814cc044707a0b57a78cb6e8b23.pdf` | (missing) |
| 第 2 行 | `id=778` `application_id=1872` `exam_name=其他` `score_text=511` `certificate_attachment_url=/api/v1/portal/attachments/student-1851/english_certificate/english_certificate-d63fa3599cac4ad587addc7cd098b4cf.pdf` | (missing) |

### candidate_no = SH20271841

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=141` `application_id=1873` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2867/english_certificate/english_certificate-ebcb5f04f47d4d76aa4b9370f6dcb447.pdf` | (missing) |

### candidate_no = SH20271842

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=48` `application_id=1874` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3005/english_certificate/english_certificate-8e57bb49083c4c128a7f9e0c2a800a93.pdf` | (missing) |

### candidate_no = SH20271843

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=827` `application_id=1875` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1782/english_certificate/english_certificate-8624eba4915843a48690f2495f6753db.pdf` | (missing) |

### candidate_no = SH20271844

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1319` `application_id=1876` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-996/english_certificate/english_certificate-9130b7c218784f4bb316c611e6013527.pdf` | (missing) |

### candidate_no = SH20271845

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1280` `application_id=1877` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1047/english_certificate/english_certificate-72b143bddb714b648553f8ff12e28612.pdf` | (missing) |

### candidate_no = SH20271846

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=101` `application_id=1878` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2924/english_certificate/english_certificate-8648833a26194b6f8326798c38eb6c0c.pdf` | (missing) |

### candidate_no = SH20271847

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=291` `application_id=1879` `exam_name=CET-6` `score_text=486` `certificate_attachment_url=/api/v1/portal/attachments/student-2653/english_certificate/english_certificate-4bfdd789b37e466d8c7829d6188f602c.pdf` | (missing) |

### candidate_no = SH20271848

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=22` `application_id=1880` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3038/english_certificate/english_certificate-a463d0430659499db9c824215b7a707a.pdf` | (missing) |

### candidate_no = SH20271849

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1260` `application_id=1881` `exam_name=CET-6` `score_text=471` `certificate_attachment_url=/api/v1/portal/attachments/student-1069/english_certificate/english_certificate-15051be463124a1b965d146e44850c42.png` | (missing) |

### candidate_no = SH20271850

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1855` `application_id=1882` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-177/english_certificate/english_certificate-9e363ef713684237a4408fbf676e0b6a.pdf` | (missing) |

### candidate_no = SH20271851

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=121` `application_id=1883` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2895/english_certificate/english_certificate-678b96d516fd4daca7f226741e46c711.pdf` | (missing) |

### candidate_no = SH20271852

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=50` `application_id=1884` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3002/english_certificate/english_certificate-eef82a11fec6460c857fdb95be0e3013.jpg` | (missing) |

### candidate_no = SH20271853

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1856` `application_id=1885` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-175/english_certificate/english_certificate-4e420340d68f49549c51b6c3efba0a0a.pdf` | (missing) |

### candidate_no = SH20271854

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1782` `application_id=1886` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-299/english_certificate/english_certificate-9f8f6cb2da2e48abb2dc3d8d55a79c21.pdf` | (missing) |

### candidate_no = SH20271855

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=648` `application_id=1887` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2071/english_certificate/english_certificate-e7fdf23358ad4e2a9dbd70799bb60a88.jpg` | (missing) |

### candidate_no = SH20271856

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=29` `application_id=1888` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3029/english_certificate/english_certificate-94b4aaac52a14d968041b394bf73344f.pdf` | (missing) |

### candidate_no = SH20271857

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=612` `application_id=1889` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2135/english_certificate/english_certificate-ff0766e4263b46bc845cf128a571d42c.pdf` | (missing) |

### candidate_no = SH20271858

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=395` `application_id=1890` `exam_name=CET-6` `score_text=605` `certificate_attachment_url=/api/v1/portal/attachments/student-2495/english_certificate/english_certificate-8599cc6ee36d4d15b32cf3b3bd2d1302.pdf` | (missing) |

### candidate_no = SH20271859

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=614` `application_id=1891` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2131/english_certificate/english_certificate-a8f3bdda69a148cb8239c13e875483ea.pdf` | (missing) |

### candidate_no = SH20271860

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=9` `application_id=1892` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3057/english_certificate/english_certificate-708c96fe48c745db9373acc7e65518b2.pdf` | (missing) |

### candidate_no = SH20271861

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=974` `application_id=1893` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1512/english_certificate/english_certificate-a0005c12db924598a7a896df35bc5ae2.pdf` | (missing) |

### candidate_no = SH20271862

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=689` `application_id=1894` `exam_name=CET-6` `score_text=595` `certificate_attachment_url=/api/v1/portal/attachments/student-2003/english_certificate/english_certificate-692e6809fd254c02b629234fb18206bd.pdf` | (missing) |

### candidate_no = SH20271863

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1211` `application_id=1895` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1135/english_certificate/english_certificate-29bdfdf7aba4441ebc14f0869dc1a2f4.pdf` | (missing) |

### candidate_no = SH20271864

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=173` `application_id=1896` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2820/english_certificate/english_certificate-c9c064efc54d4333af502629acb78c5a.pdf` | (missing) |

### candidate_no = SH20271865

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=846` `application_id=1897` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1745/english_certificate/english_certificate-010d3a1b361f4d31814bd900d8f6e606.pdf` | (missing) |

### candidate_no = SH20271866

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1716` `application_id=1898` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-416/english_certificate/english_certificate-ec4366e1291e4f5896b369c53bf4d36a.pdf` | (missing) |

### candidate_no = SH20271867

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=158` `application_id=1899` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2843/english_certificate/english_certificate-0b80fc5bb3994f809c8304284ef83c7a.pdf` | (missing) |

### candidate_no = SH20271868

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=25` `application_id=1900` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3034/english_certificate/english_certificate-5b88b90a70a447f281021124a0bfab34.pdf` | (missing) |

### candidate_no = SH20271869

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=115` `application_id=1901` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2902/english_certificate/english_certificate-270b7e34ce16469cbdce24ed530cde08.pdf` | (missing) |

### candidate_no = SH20271870

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=330` `application_id=1902` `exam_name=CET-6` `score_text=440` `certificate_attachment_url=/api/v1/portal/attachments/student-2599/english_certificate/english_certificate-76f522d5b3074a5bb67a861b506f9464.pdf` | (missing) |
| 第 2 行 | `id=331` `application_id=1902` `exam_name=其他` `score_text=68` `certificate_attachment_url=/api/v1/portal/attachments/student-2599/english_certificate/english_certificate-3fea2ce5d97e44ce87c4f19085e7a3eb.pdf` | (missing) |

### candidate_no = SH20271871

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=438` `application_id=1903` `exam_name=CET-6` `score_text=571` `certificate_attachment_url=/api/v1/portal/attachments/student-2400/english_certificate/english_certificate-7b4ce4ee537e4970bbd752c1d5343d6a.pdf` | (missing) |

### candidate_no = SH20271872

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1220` `application_id=1904` `exam_name=CET-6` `score_text=518` `certificate_attachment_url=/api/v1/portal/attachments/student-1123/english_certificate/english_certificate-3fe99f58fc994327b330131787051538.pdf` | (missing) |
| 第 2 行 | `id=1221` `application_id=1904` `exam_name=其他` `score_text=597` `certificate_attachment_url=/api/v1/portal/attachments/student-1123/english_certificate/english_certificate-8e7e59ed1d244f4392a2546c61481ba4.pdf` | (missing) |

### candidate_no = SH20271873

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=10` `application_id=1905` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3056/english_certificate/english_certificate-ec610de84e6e4213a154a2c4f6b563d8.pdf` | (missing) |

### candidate_no = SH20271874

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=109` `application_id=1906` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2910/english_certificate/english_certificate-29b25415ac4840a48fea4f1a06672159.pdf` | (missing) |

### candidate_no = SH20271875

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=867` `application_id=1907` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1711/english_certificate/english_certificate-a3cb04088abe40448db308bce44b2d05.pdf` | (missing) |

### candidate_no = SH20271876

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=661` `application_id=1908` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2055/english_certificate/english_certificate-94c3fd42f49b4b45889e1b5a3192aa9a.pdf` | (missing) |

### candidate_no = SH20271877

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=54` `application_id=1909` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2997/english_certificate/english_certificate-8a4752f0d88c4d1e8db32aae4b094127.pdf` | (missing) |

### candidate_no = SH20271878

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=62` `application_id=1910` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2986/english_certificate/english_certificate-c6cc10cd2bd6467c945e2bf2612033c1.pdf` | (missing) |

### candidate_no = SH20271879

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=132` `application_id=1911` `exam_name=CET-6` `score_text=454` `certificate_attachment_url=/api/v1/portal/attachments/student-2881/english_certificate/english_certificate-92ddb541973c4c96ad7310cb418adbd1.pdf` | (missing) |

### candidate_no = SH20271880

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1412` `application_id=1912` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-867/english_certificate/english_certificate-cc878904919e4053a14fe0be8d2750ff.pdf` | (missing) |

### candidate_no = SH20271881

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=12` `application_id=1913` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3054/english_certificate/english_certificate-55f1ec291c754b779ae54fba715a8cdd.pdf` | (missing) |

### candidate_no = SH20271882

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=406` `application_id=1914` `exam_name=CET-6` `score_text=542` `certificate_attachment_url=/api/v1/portal/attachments/student-2474/english_certificate/english_certificate-da3dc1fab19f468cb6f38eb74167163e.pdf` | (missing) |

### candidate_no = SH20271883

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=20` `application_id=1915` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3040/english_certificate/english_certificate-c9fd81b29b234ef9b6ff886fc6871cc8.pdf` | (missing) |

### candidate_no = SH20271884

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=100` `application_id=1916` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2925/english_certificate/english_certificate-21a518dc1676440eb22d9d452980f369.pdf` | (missing) |

### candidate_no = SH20271885

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=686` `application_id=1917` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2009/english_certificate/english_certificate-5a5bab67df554a62a8265baf644c2dec.pdf` | (missing) |

### candidate_no = SH20271886

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=411` `application_id=1918` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2461/english_certificate/english_certificate-60dab8666cc147b695422c007aa08290.jpg` | (missing) |

### candidate_no = SH20271887

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=263` `application_id=1919` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2688/english_certificate/english_certificate-a21244747e38441297abb8d4d10456f4.pdf` | (missing) |

### candidate_no = SH20271888

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=67` `application_id=1920` `exam_name=CET-6` `score_text=464` `certificate_attachment_url=/api/v1/portal/attachments/student-2975/english_certificate/english_certificate-ddf7a9182eb24066a5ddcc13e164a5c0.pdf` | (missing) |

### candidate_no = SH20271889

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=99` `application_id=1921` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2928/english_certificate/english_certificate-9c4573ae9f204b01abbe5c0369df098e.pdf` | (missing) |

### candidate_no = SH20271890

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=635` `application_id=1922` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2090/english_certificate/english_certificate-283531d265bf4e658ad953900a31b438.pdf` | (missing) |

### candidate_no = SH20271891

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=30` `application_id=1923` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3027/english_certificate/english_certificate-904cd34b03834b5794df85e477b9fd97.pdf` | (missing) |

### candidate_no = SH20271892

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1243` `application_id=1924` `exam_name=CET-6` `score_text=513` `certificate_attachment_url=/api/v1/portal/attachments/student-1091/english_certificate/english_certificate-883138e5b8df44e486fe6622b9211aa6.pdf` | (missing) |

### candidate_no = SH20271893

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=255` `application_id=1925` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2701/english_certificate/english_certificate-27831fe3af95400bba927246995927a3.pdf` | (missing) |

### candidate_no = SH20271894

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=480` `application_id=1926` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2337/english_certificate/english_certificate-4902ba3131ec4274a9c5aff0195ff9ab.pdf` | (missing) |

### candidate_no = SH20271895

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1179` `application_id=1927` `exam_name=CET-6` `score_text=525` `certificate_attachment_url=/api/v1/portal/attachments/student-1194/english_certificate/english_certificate-debd55e123cd447dabd6056b50eac32c.png` | (missing) |

### candidate_no = SH20271896

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=696` `application_id=1928` `exam_name=CET-6` `score_text=468` `certificate_attachment_url=/api/v1/portal/attachments/student-1984/english_certificate/english_certificate-1144e35dce51457abc228a616aab9612.pdf` | (missing) |

### candidate_no = SH20271897

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1761` `application_id=1929` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-342/english_certificate/english_certificate-67407d9a020d4fc99463ff8e180a0104.pdf` | (missing) |

### candidate_no = SH20271898

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=217` `application_id=1930` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2752/english_certificate/english_certificate-87f1ae55e5d54897ba5548ebf7f60141.pdf` | (missing) |

### candidate_no = SH20271899

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=944` `application_id=1931` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1571/english_certificate/english_certificate-11e333e7324549bba11fd581c058a522.pdf` | (missing) |

### candidate_no = SH20271900

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=19` `application_id=1932` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3042/english_certificate/english_certificate-0caed2c9f52e400fab532c2b3f243321.pdf` | (missing) |

### candidate_no = SH20271901

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=552` `application_id=1933` `exam_name=CET-6` `score_text=604` `certificate_attachment_url=/api/v1/portal/attachments/student-2233/english_certificate/english_certificate-da20936fc3ae49e7a9ca6527e69a4960.pdf` | (missing) |

### candidate_no = SH20271902

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1289` `application_id=1934` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1038/english_certificate/english_certificate-179c14d238a44cebadd51539df757585.pdf` | (missing) |

### candidate_no = SH20271903

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=33` `application_id=1935` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3024/english_certificate/english_certificate-1b66a87ef03f4213950120ccbe74fc07.pdf` | (missing) |

### candidate_no = SH20271904

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=188` `application_id=1936` `exam_name=CET-6` `score_text=500` `certificate_attachment_url=/api/v1/portal/attachments/student-2790/english_certificate/english_certificate-3bbf089cc198427bb6192a0b2e9a0073.pdf` | (missing) |

### candidate_no = SH20271905

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=6` `application_id=1937` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3060/english_certificate/english_certificate-7d322618682f41f380469cd9cb59c64c.pdf` | (missing) |

### candidate_no = SH20271906

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=7` `application_id=1938` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3059/english_certificate/english_certificate-127b65e7fe5f4c93b67c4669b956a634.pdf` | (missing) |

### candidate_no = SH20271907

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=341` `application_id=1939` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2588/english_certificate/english_certificate-d3da8805452f4438adef36a69874b889.pdf` | (missing) |

### candidate_no = SH20271908

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=71` `application_id=1940` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2969/english_certificate/english_certificate-172733d2d19d49a3ad0891cc320f138f.pdf` | (missing) |

### candidate_no = SH20271909

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=107` `application_id=1941` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2914/english_certificate/english_certificate-30865ac616df4ba2a3bbdfca462dcf8d.pdf` | (missing) |

### candidate_no = SH20271910

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=5` `application_id=1942` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3069/english_certificate/english_certificate-c825f6b1dc384bf9a5ea7015eb2da28a.jpg` | (missing) |

### candidate_no = SH20271911

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1265` `application_id=1943` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1065/english_certificate/english_certificate-a3e0393c1d984c1ab535edc1d44fb63c.pdf` | (missing) |

### candidate_no = SH20271912

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1805` `application_id=1944` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-258/english_certificate/english_certificate-a079d4d27f2a49ffaac5bec7b0f6f9b1.pdf` | (missing) |

### candidate_no = SH20271913

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1982` `application_id=1986` `exam_name=CET-6` `score_text=447` `certificate_attachment_url=/api/v1/portal/attachments/student-234/english_certificate/english_certificate-2ab1aee8b7f3412794a7c7bdc0747d20.pdf` | (missing) |

### candidate_no = SH20271914

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=8` `application_id=1946` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3058/english_certificate/english_certificate-899cc2861bdd47fca27bd04d174889e2.pdf` | (missing) |

### candidate_no = SH20271915

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=982` `application_id=1947` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1502/english_certificate/english_certificate-94b0eead415447518ee99a038fa8df99.jpg` | (missing) |

### candidate_no = SH20271916

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1637` `application_id=1948` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-535/english_certificate/english_certificate-a9202173cca8424aa309bb3bb2ff831d.pdf` | (missing) |

### candidate_no = SH20271917

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1415` `application_id=1949` `exam_name=TOEFL` `score_text=100` `certificate_attachment_url=/api/v1/portal/attachments/student-864/english_certificate/english_certificate-9181e8586625465f93684de32335e11e.pdf` | (missing) |

### candidate_no = SH20271918

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=699` `application_id=1950` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1980/english_certificate/english_certificate-d5647ecdc940411a834f0f4d91e30768.pdf` | (missing) |

### candidate_no = SH20271919

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=11` `application_id=1951` `exam_name=CET-6` `score_text=535` `certificate_attachment_url=/api/v1/portal/attachments/student-3055/english_certificate/english_certificate-7fed06512e78472e88b67613ec1e5d85.pdf` | (missing) |

### candidate_no = SH20271920

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=96` `application_id=1952` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2931/english_certificate/english_certificate-20e0ad1724b84fca9e63da5a7dcaa90c.pdf` | (missing) |

### candidate_no = SH20271921

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=103` `application_id=1953` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2919/english_certificate/english_certificate-5a23dc7f53134782add536235d40d044.pdf` | (missing) |

### candidate_no = SH20271922

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=304` `application_id=1954` `exam_name=CET-6` `score_text=614` `certificate_attachment_url=/api/v1/portal/attachments/student-2634/english_certificate/english_certificate-e137f9b72bdd45a5addb0380b09822ec.pdf` | (missing) |

### candidate_no = SH20271923

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=647` `application_id=1955` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2072/english_certificate/english_certificate-037821ff4e7a4defbdaa520bc3cb9f29.pdf` | (missing) |

### candidate_no = SH20271924

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=128` `application_id=1956` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2885/english_certificate/english_certificate-99eed47fe0604eac90d126367842ffcb.pdf` | (missing) |

### candidate_no = SH20271925

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=531` `application_id=1957` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2260/english_certificate/english_certificate-226119bec13c4943a955ae34efd47c92.pdf` | (missing) |

### candidate_no = SH20271926

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1523` `application_id=1958` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-707/english_certificate/english_certificate-7f3ff5a9e3434e0184dc04252c96b07f.png` | (missing) |

### candidate_no = SH20271927

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=218` `application_id=1959` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2750/english_certificate/english_certificate-36dfcf603b8e4f8bb99e7aa05323c0bc.pdf` | (missing) |

### candidate_no = SH20271928

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=829` `application_id=1960` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1778/english_certificate/english_certificate-878ee9b9e1fa4f7d979d716baf574499.jpg` | (missing) |

### candidate_no = SH20271929

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1247` `application_id=1961` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1087/english_certificate/english_certificate-b03ecb94f5c94e8ea048f76481802c18.pdf` | (missing) |

### candidate_no = SH20271930

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=32` `application_id=1962` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3025/english_certificate/english_certificate-33f1d965262543ea8160833ec5b86b77.pdf` | (missing) |

### candidate_no = SH20271931

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1489` `application_id=1963` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-759/english_certificate/english_certificate-50afd81ccd2c4cebae640f64974b65bb.jpg` | (missing) |

### candidate_no = SH20271932

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=338` `application_id=1964` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2591/english_certificate/english_certificate-8c237bc9d08947b38b3df53f8e6a0d6b.pdf` | (missing) |

### candidate_no = SH20271933

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=732` `application_id=1965` `exam_name=IELTS` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1924/english_certificate/english_certificate-4cb22aba590246479d0e455da1dfa383.jpg` | (missing) |

### candidate_no = SH20271934

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=147` `application_id=1966` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2858/english_certificate/english_certificate-5dbf8710457c4f2987ecad2edfd8679f.pdf` | (missing) |

### candidate_no = SH20271935

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1256` `application_id=1967` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-1075/english_certificate/english_certificate-8a61987391d44a8f86a0efdf8fd06631.pdf` | (missing) |

### candidate_no = SH20271936

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=578` `application_id=1968` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2187/english_certificate/english_certificate-8c039a1314084228b25e63dc7377421c.pdf` | (missing) |

### candidate_no = SH20271937

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=4` `application_id=1969` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3070/english_certificate/english_certificate-dc860e0d09fc4dc38379fded1d7deb64.pdf` | (missing) |

### candidate_no = SH20271938

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=3` `application_id=1970` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3073/english_certificate/english_certificate-5defa366a5274a9681613b6ef0d732d7.jpg` | (missing) |

### candidate_no = SH20271939

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=512` `application_id=1971` `exam_name=TOEFL` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2284/english_certificate/english_certificate-3b25cf5eae0a4c0b908bcc6cdee2eb54.pdf` | (missing) |

### candidate_no = SH20271940

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1521` `application_id=1972` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-712/english_certificate/english_certificate-026b8d1b71634c93ae54c91d5f01b0a4.pdf` | (missing) |

### candidate_no = SH20271941

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=427` `application_id=1973` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2422/english_certificate/english_certificate-01aa3b915d0b4e3d8f9cfcb59115796f.png` | (missing) |

### candidate_no = SH20271942

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=43` `application_id=1974` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-3011/english_certificate/english_certificate-28ff64ba0fb9424a8f3845b6b06ea70f.pdf` | (missing) |

### candidate_no = SH20271943

- 主库行数：2
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1984` `application_id=1987` `exam_name=IELTS` `score_text=7.0` `certificate_attachment_url=/api/v1/portal/attachments/student-3152/english_certificate/english_certificate-c3c8b3172c914b85bff660dfceafd32f.jpg` | (missing) |
| 第 2 行 | `id=1985` `application_id=1987` `exam_name=CET-6` `score_text=588` `certificate_attachment_url=/api/v1/portal/attachments/student-3152/english_certificate/english_certificate-cf0d7ff0bc354c1ab32e8fd2fcd2e912.pdf` | (missing) |

### candidate_no = SH20271944

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=2` `application_id=1976` `exam_name=其他` `score_text=100` `certificate_attachment_url=/api/v1/portal/attachments/student-3081/english_certificate/english_certificate-22996c2f38be457685d0e1ce892b7495.pdf` | (missing) |

### candidate_no = SH20271945

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=380` `application_id=1977` `exam_name=CET-6` `score_text=502` `certificate_attachment_url=/api/v1/portal/attachments/student-2529/english_certificate/english_certificate-25c7c70f16fb44098e958eebfbba067e.pdf` | (missing) |

### candidate_no = SH20271946

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=274` `application_id=1978` `exam_name=CET-6` `score_text=(empty)` `certificate_attachment_url=/api/v1/portal/attachments/student-2674/english_certificate/english_certificate-1d74c7bb9b99489c80a80d2655220304.pdf` | (missing) |

### candidate_no = SH20271947

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1` `application_id=1979` `exam_name=CET-6` `score_text=523` `certificate_attachment_url=/api/v1/portal/attachments/student-3110/english_certificate/english_certificate-70f05ef728f4468797ef85e6b45c4df1.pdf` | (missing) |

### candidate_no = SH20271948

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1974` `application_id=1980` `exam_name=CET-6` `score_text=583` `certificate_attachment_url=/api/v1/portal/attachments/student-2645/english_certificate/english_certificate-eb59821de9b1406faa07144b91187bf6.png` | (missing) |

### candidate_no = SH20271949

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1975` `application_id=1981` `exam_name=CET-6` `score_text=528` `certificate_attachment_url=/api/v1/portal/attachments/student-3083/english_certificate/english_certificate-9905861958bc4321bdf00e121eda1555.pdf` | (missing) |

### candidate_no = SH20271950

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1976` `application_id=1982` `exam_name=CET-6` `score_text=581` `certificate_attachment_url=/api/v1/portal/attachments/student-3124/english_certificate/english_certificate-f899b606ad0448f9983448f5580cee9a.pdf` | (missing) |

### candidate_no = SH20271951

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1977` `application_id=1983` `exam_name=CET-6` `score_text=464` `certificate_attachment_url=/api/v1/portal/attachments/student-3128/english_certificate/english_certificate-1e1e2d1276654444b5b6d9dde46e5e0c.pdf` | (missing) |

### candidate_no = SH20271952

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1978` `application_id=1984` `exam_name=CET-6` `score_text=547` `certificate_attachment_url=/api/v1/portal/attachments/student-3129/english_certificate/english_certificate-a451cd6e3dad46a2ba398736c695a5b1.pdf` | (missing) |

### candidate_no = SH20271953

- 主库行数：1
- 备库行数：0
- 附件 URL 是否一致：是

| 位置 | 主库 | 备库 |
| --- | --- | --- |
| 第 1 行 | `id=1979` `application_id=1985` `exam_name=CET-6` `score_text=443` `certificate_attachment_url=/api/v1/portal/attachments/student-3095/english_certificate/english_certificate-5789fe5c8cba4c04a3fa8d0d5b5422e9.png` | (missing) |

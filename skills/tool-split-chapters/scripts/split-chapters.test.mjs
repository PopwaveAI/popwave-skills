import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
import { after, before, describe, test } from "node:test";

/**
 * 分章归一（tool-split-chapters）确定性脚本的端到端测试。
 * 用 child_process 真实调用 CLI，在临时目录里驱动自造 fixture，
 * 断言产物（manifest / chapters / 索引 / 指纹 / 批次计划）的结构与判定。
 */

const SCRIPT_PATH = fileURLToPath(new URL("./split-chapters.mjs", import.meta.url));
const SCRIPT_DIR = path.dirname(SCRIPT_PATH);

/** GBK 字节（「第一章 风起 / 第二章 雨落 / 第三章 归途」三章样例）的 base64 */
const GBK_FIXTURE_BASE64 =
  "tdrSu9XCILfnxvAKydnE6sGi09rJveHbo6zN+9fF1Ma6o7et07+howrL+9aqtcCjrL3xyNXWrrrzo6zU2c7eu9jNt8K3oaMKtdq2/tXCINPqwuQK0+q149TS1NrH4MqvsOXJz6OsvabG8M+4y+nLrruooaMKy/2zxdfF083Wvcmho6zVvtTaz++/2rXIwcu63L7DoaMKtdrI/dXCILnpzb4Kwu3M48n508nUtrywvfyhowrL+9bV09q72MC0wcujrLT418XC+sntt+ezvqGjCg==";

const tempRoot = mkdtempSync(path.join(os.tmpdir(), "popwave-split-chapters-"));
const fixtureDir = path.join(tempRoot, "fixtures");

function runCli(args) {
  const result = spawnSync(process.execPath, [SCRIPT_PATH, ...args], { encoding: "utf8" });
  return { code: result.status ?? -1, stdout: result.stdout ?? "", stderr: result.stderr ?? "" };
}

function fixturePath(name) {
  return path.join(fixtureDir, name);
}

function writeFixture(name, content) {
  const filePath = fixturePath(name);
  writeFileSync(filePath, content, "utf8");
  return filePath;
}

function outDir(name) {
  return path.join(tempRoot, "out", name);
}

function readJson(filePath) {
  return JSON.parse(readFileSync(filePath, "utf8"));
}

function readManifest(dir) {
  return readJson(path.join(dir, "manifest.json"));
}

/** 递归收集 JSON 里的全部键名（含嵌套对象与数组元素），用于守卫 JSON 契约的命名风格 */
function collectJsonKeys(value, at, sink) {
  if (Array.isArray(value)) {
    value.forEach((item, index) => collectJsonKeys(item, `${at}[${index}]`, sink));
    return;
  }
  if (value && typeof value === "object") {
    for (const [key, child] of Object.entries(value)) {
      const here = at ? `${at}.${key}` : key;
      sink.push({ key, where: here });
      collectJsonKeys(child, here, sink);
    }
  }
}

/** 跑一次 CLI 并要求成功，返回 manifest 与运行摘要 */
function split(dir, args) {
  const target = outDir(dir);
  const result = runCli([...args, "--out", target, "--json"]);
  assert.strictEqual(result.stderr, "");
  assert.strictEqual(result.code, 0);
  const summary = JSON.parse(result.stdout);
  return { manifest: readManifest(target), summary };
}

const STANDARD_BOOK = [
  "测试书",
  "",
  "第一卷 风起卷",
  "",
  "第一章 起点",
  "少年立于山巅，望着云海翻涌。他知道，今日之后，再无回头路可走。",
  "风从谷底吹上来，卷起衣角。",
  "",
  "第二章 试炼",
  "剑光如雪，落在青石上溅起火星。他咬着牙，把最后一式走完。",
  "师父站在远处，没有说话。",
  "",
  "第三章 下山",
  "山门在身后合拢。他背起行囊，头也不回。",
  "山下有市集，有酒旗，也有他从未见过的江湖。",
  "",
  "第二卷 江湖卷",
  "",
  "第四章 初见",
  "客栈里人声嘈杂，说书人拍着醒木。",
  "他坐在角落，听了一整夜。",
  "",
  "第五章 交手",
  "刀锋擦着耳畔掠过，他侧身避过，反手一拳砸在对方肋下。",
  "两人同时后退半步。",
  "",
  "第六章 归途",
  "雪落在他的肩上，融化成水。",
  "远处城门的灯火，像那年他离开时一样。",
  "",
].join("\n");

const NO_HEADING_BOOK = [
  "落日的余晖洒在青石板上，街市渐渐安静下来。",
  "少年背着包，一路向西走，脚步不快也不慢。",
  "他想起很多年前的一个傍晚，母亲站在门口，喊他回家吃饭。",
  "那时候他还小，觉得日子长得很，怎么也走不到头。",
  "如今路边的柳树已经长得很高，风吹过来的时候，枝条轻轻扫过他的肩膀。",
  "他没有回头，只是把手里的东西攥得更紧了些。",
  "前方是一片矮山，山脚下有条小河，河水安静地流着。",
  "他蹲下来洗了把脸，水很凉，凉得他心里那点焦躁也散了些。",
  "远处有人在喊船，声音顺着水面飘过来，听不太真切。",
  "他站起身，拍了拍膝盖上的土，继续往前走。",
  "天完全黑下来的时候，他终于看见了对岸的灯火，一盏接着一盏，连成一片。",
  "他在渡口等了很久，船才靠过来，船夫是个上了年纪的老人，什么也没问。",
  "他坐上船，看着水面上的灯影一晃一晃，忽然觉得这就是他要去的地方。",
  "船靠岸的时候，他把钱放在船板上，起身跳下船，头也不回地走进了码头的人流里。",
  "",
].join("\n");

const REPEATED_TITLE_BOOK = [
  "第一章 起",
  "正文内容足够长，避免被判为正文缺失，这里只是占位。",
  "",
  "第三章 重逢",
  "重逢的正文，长度足够，不会被判为正文缺失。",
  "",
  "第三章 重逢",
  "同样的标题又出现了一次，用于验证重复章名检测。",
  "正文长度也足够。",
  "",
].join("\n");

const ROMAN_TITLE_BOOK = [
  "第一章 正常开篇",
  "正常正文，长度足够，不会被判为正文缺失，这里只是占位。",
  "第XII章 罗马数字",
  "这一章的标题用了罗马数字，脚本的标题正则识别不了它。",
  "第三章 正常三",
  "正常正文，长度足够，不会被判为正文缺失，这里只是占位。",
  "",
].join("\n");

const REVISION_BASE_BOOK = [
  "第一章 甲",
  "甲字正文占位，长度足够二十个非空白字符，避免被判为正文缺失。",
  "",
  "第二章 乙",
  "乙字正文占位，长度足够二十个非空白字符，避免被判为正文缺失。",
  "",
  "第三章 丙",
  "丙字正文占位，长度足够二十个非空白字符，避免被判为正文缺失。",
  "",
  "第四章 丁",
  "丁字正文占位，长度足够二十个非空白字符，避免被判为正文缺失。",
  "",
].join("\n");

function buildManyChapterBook(count) {
  const lines = [];
  for (let i = 1; i <= count; i += 1) {
    lines.push(`第${i}章 第${i}段`);
    lines.push(`这是第 ${i} 章的正文占位内容，长度足够，避免被判为正文缺失，也不制造噪声。`);
    lines.push("");
  }
  return lines.join("\n");
}

/**
 * 《道诡异仙》式 Markdown 排版（自造 fixture，真实素材不入仓）：
 * `#{1,6}` 标题 / `**加粗**` 标题 / 不含章节号的非章标题 / `******` 分隔符 / 内部卷标记。
 * 行号即断言用的行号：L5 上架感言、L14 番外、L20 分隔符、L22 卷标记。
 */
const MARKDOWN_BOOK = [
  "# 第一章 师傅", // L1
  "李火旺举起手中的捣药杆，百无聊赖地一下一下砸在捣药罐里，把夹杂着淤泥的流光青石碾成粉末。", // L2
  "洞内潮湿寒冷，少年却满脸不在乎，似乎并没把这一切放在眼里。", // L3
  "", // L4
  "# 上架感言", // L5 非章标题（author-note）
  "明天就要上架了，感谢各位读者一直以来的支持，希望大家多多订阅。", // L6
  "", // L7
  "## 第二章 雨落", // L8 二级标题
  "雨点砸在青石板上，溅起细碎的水花，路人纷纷跑开，屋檐下的猫也缩了回去。", // L9
  "", // L10
  "**第三章 夜行**", // L11 Markdown + 加粗
  "夜色像墨一样浓，他提着灯笼走在没有尽头的巷子里，脚下的青石板泛着湿光。", // L12
  "", // L13
  "# 番外：清旺来", // L14 非章标题（side-story）
  "这是作者随手写的番外，跟主线没有任何关系，只是练笔而已。", // L15
  "", // L16
  "# 第四章 收尾", // L17
  "故事到这里就告一段落了，他终于把药杵放下，抬头看了看洞外的天光。", // L18
  "", // L19
  "******", // L20 分隔符，不是标题
  "", // L21
  "第一卷（完）", // L22 内部卷标记
].join("\n");

/**
 * 混合两种来源（Markdown 标题 + 裸标题）：含重号（第一百二十章 两次）、缺号（缺 121）、
 * 盗版站残留后缀、正常标题里的「免费阅读」、非章标题与内部卷标记。
 * 行号：L7 裸标题+残留、L13 正常标题含残留字眼、L16 非章标题、L19 分隔符、L21 卷标记。
 */
const MIXED_SOURCE_BOOK = [
  "# 第一章 师傅", // L1
  "李火旺把捣药杆放下，抬头看向洞外的天光，心里慢慢有了一个主意。", // L2
  "", // L3
  "# 第一百二十章 伤口", // L4
  "伤口已经结痂，他却总觉得里面还在隐隐作痛，像有什么东西没取出来。", // L5
  "", // L6
  "第一百二十章 伤口免费阅读.", // L7 裸标题 + 盗版残留（重号）
  "这具身体的原主人留给他的记忆正在慢慢消退，只剩下一些模糊的碎片。", // L8
  "", // L9
  "# 第一百二十二章 赶路", // L10
  "山路崎岖，他背着行囊走了整整一天，直到天边泛白才看见远处的村镇。", // L11
  "", // L12
  "# 第一百二十三章 免费阅读的秘密", // L13 正常标题里的残留字眼不可误删
  "标题里本来就带着这几个字，它们是正文的一部分，不能被当成站点残留清掉。", // L14
  "", // L15
  "# 抱歉", // L16 非章标题
  "今天临时有事，更新要晚一点，明天补上，各位读者朋友早点休息。", // L17
  "", // L18
  "******", // L19 分隔符
  "", // L20
  "第二卷(完)", // L21 内部卷标记
].join("\n");

/** 作者公告里带「1、2、4、5、」编号清单（缺 3）：有强章边界时不得采纳为章。 */
const NOTE_NUMBERED_LIST_BOOK = [
  "# 第一章 师傅", // L1
  "李火旺把捣药杆放下，抬头看向洞外的天光，心里有了一个主意。", // L2
  "# 关于抖音直播", // L3 非章标题
  "在正文之外插一条活动公告，公告里带着编号清单：", // L4
  "1、关注这《道诡异仙》抖音账号，并预约9.29日晚上7点的直播；", // L5
  "2、将关注、直播预约截图回复至评论区，一个起点账号只计算一次；", // L6
  "4、所有合格参与者平分活动奖励；", // L7
  "5、奖励上限者不再进行补发。", // L8
  "活动解释权归作者所有，感谢各位配合。", // L9
  "", // L10
  "# 第二章 雨落", // L11
  "雨点砸在青石板上，溅起细碎的水花，路人纷纷跑开。", // L12
].join("\n");

/** 作者感言里出现「第二卷」+「完」：不是卷边界，也不是内部卷标记。 */
const VOLUME_REMARK_BOOK = [
  "# 第一章 甲", // L1
  "甲的正文内容，长度足够二十个非空白字符，用来避免被判为正文过短。", // L2
  "第二卷写完了，嗯…那我就歇一天吧。还望各位见谅", // L3 作者感言
  "# 第二章 乙", // L4
  "乙的正文内容，长度足够二十个非空白字符，用来避免被判为正文过短。", // L5
].join("\n");

/**
 * 盗版 / 抓取痕迹样本：报错浮层 4 行 + 纯 URL 行 + 分页重复标题 + 正文里含噪声词（不该被删）。
 * 行号：L1–L4 浮层、L7 纯 URL、L8/L10 分页重复标题、L12 正文含「最新章节」。
 */
const CLEANING_BOOK = [
  "请选择错误类型", // L1
  "更新太慢", // L2
  "缺少章节", // L3
  "章节内容错误", // L4
  "第一章 风起", // L5
  "少年立于山巅，望着云海翻涌，他知道今日之后再无回头路可走。", // L6
  "www.pirate-site.com", // L7
  "第二章 雨落（第1/2页）", // L8
  "雨点砸在青石板上，溅起细碎的水花，路人纷纷跑开躲雨。", // L9
  "第二章 雨落（第2/2页）", // L10
  "他把伞递给老人，自己淋着雨往前走，鞋里全是水。", // L11
  "他合上书说：这本要收费才能看最新章节。", // L12 正文含噪声词，不该被删
  "第三章 归途", // L13
  "雪落在他的肩上，融化成水，远处城门的灯火连成一片。", // L14
  "",
].join("\n");

/**
 * 目录块样本：L1–L3 是目录（标题与后文真章一致、自身无正文），L5/L7/L9 才是真章。
 * 目录用中文数字、真章用补零数字，正好考「标题比较键要剥掉『第X章』前缀」。
 */
const CLEANING_TOC_BOOK = [
  "第一章 风起", // L1 目录
  "第二章 雨落", // L2 目录
  "第三章 归途", // L3 目录
  "", // L4
  "第001章 风起", // L5 真章
  "少年立于山巅，望着云海翻涌，他知道今日之后再无回头路可走。", // L6
  "第002章 雨落", // L7
  "雨点砸在青石板上，溅起细碎的水花，路人纷纷跑开躲雨。", // L8
  "第003章 归途", // L9
  "雪落在他的肩上，融化成水，远处城门的灯火连成一片。", // L10
  "",
].join("\n");

before(() => {
  assert.ok(existsSync(SCRIPT_PATH), `脚本不存在：${SCRIPT_PATH}`);
  mkdirSync(fixtureDir, { recursive: true });
  writeFixture("standard.txt", STANDARD_BOOK);
  writeFixture("noheadings.txt", NO_HEADING_BOOK);
  writeFixture("repeated.txt", REPEATED_TITLE_BOOK);
  writeFixture("roman.txt", ROMAN_TITLE_BOOK);
  writeFixture("revision-base.txt", REVISION_BASE_BOOK);
  writeFixture("many.txt", buildManyChapterBook(45));
  writeFixture("mdbook.txt", MARKDOWN_BOOK);
  writeFixture("mixedbook.txt", MIXED_SOURCE_BOOK);
  writeFixture("notelist.txt", NOTE_NUMBERED_LIST_BOOK);
  writeFixture("volremark.txt", VOLUME_REMARK_BOOK);
  writeFixture("cleaning.txt", CLEANING_BOOK);
  writeFixture("cleaning-toc.txt", CLEANING_TOC_BOOK);
  writeFixture("vol1.txt", ["第一章 初见", "雨后的巷子很安静，只有屋檐上还在滴水。", "", "第二章 相知", "两个人坐在灯下，一个写字，一个磨墨。", "", "第三章 别离", "码头上风很大。她把包袱递给他，说路上小心。", ""].join("\n"));
  writeFixture("vol2.txt", ["第四章 重逢", "又是雨天，他站在同一条巷子里，抬手，敲门。", "", "第五章 终局", "很多年以后，有人问起那本书的下落。", ""].join("\n"));
  // 跨资产对齐用 fixture：编号重叠（vol1 = 1..3，本卷 2..3 → 重叠 2 章）
  writeFixture("overlap.txt", ["第二章 试炼", "重叠卷的第二章正文，长度足够二十个非空白字符，用于占位。", "", "第三章 下山", "重叠卷的第三章正文，长度足够二十个非空白字符，用于占位。", ""].join("\n"));
  // 每卷从第一章重新编号（分卷常见排版）
  writeFixture("restart.txt", ["第一章 另一条线", "另一条线的第一章正文，长度足够二十个非空白字符，用于占位。", "", "第二章 继续", "另一条线的第二章正文，长度足够二十个非空白字符，用于占位。", ""].join("\n"));
  // 跨卷同章名（正文不同，避免被指纹去重跳过）
  writeFixture("same-title-a.txt", ["第一章 同题", "甲版本的正文，长度足够二十个非空白字符，用于占位。", ""].join("\n"));
  writeFixture("same-title-b.txt", ["第一章 同题", "乙版本的正文，长度足够二十个非空白字符，用于占位。", ""].join("\n"));
  // 完全相同的两份内容（文件名不同），用于指纹去重
  const duplicateBody = ["第一章 同源", "正文正文正文正文正文正文正文正文正文正文正文正文正文正文。", "", "第二章 同源之二", "又是正文，长度足够，不会被判定为正文缺失，也不会触发裁决。", ""].join("\n");
  writeFixture("dupA.txt", duplicateBody);
  writeFixture("dupB-副本.txt", duplicateBody);
  // CRLF + 全角数字标题
  writeFixture("crlf.txt", ["第１章 全角风起", "正文内容，长度足够，避免被判为正文缺失，一切都好。", "", "第２章 全角雨落", "雨点砸在青石板上，溅起细碎的水花，路人纷纷跑开。", ""].join("\r\n"));
  // GBK 字节
  writeFileSync(fixturePath("gbk.txt"), Buffer.from(GBK_FIXTURE_BASE64, "base64"));
  // JSON 键名守卫用 fixture：资产 ID 全部是 ASCII 小写字母，键名正则才不会误伤动态键（encoding.assets / meta.leadingText 等按 assetId 取键）
  writeFixture(
    "guardmain.txt",
    [
      "第一章 开篇",
      "这里是一段足够长的正文占位内容，用来避免被判定为正文过短或缺失。",
      "第XII章 罗马数字",
      "这一章的标题用了罗马数字，脚本的标题正则识别不了它，因此会记入未识别标题行。",
      "第三章 重现",
      "同样的标题重复出现，用来触发重复章名与编号乱序的判定逻辑。",
      "第三章 重现",
      "请记住本站，正文里混进了站点污染行，用来触发污染检测分支。",
      "第四章 很短",
      "短",
      "",
    ].join("\n"),
  );
  writeFixture(
    "guardnum.txt",
    [
      "1、第一段",
      "这是第一段的正文占位内容，长度足够二十个非空白字符以避免被判短。",
      "2、第二段",
      "这是第二段的正文占位内容，长度足够二十个非空白字符以避免被判短。",
      "3、第三段",
      "这是第三段的正文占位内容，长度足够二十个非空白字符以避免被判短。",
      "",
    ].join("\n"),
  );
  const guardDuplicateBody = [
    "第一章 同源",
    "正文内容足够长，用来占位，避免被判为正文过短或缺失。",
    "",
    "第二章 同源之二",
    "又是正文，长度足够，不会被判定为正文缺失，也不会触发裁决。",
    "",
  ].join("\n");
  writeFixture("guarda.txt", guardDuplicateBody);
  writeFixture("guardb.txt", guardDuplicateBody);
  // 同名不同内容的两份资产（放在不同子目录），用于指纹后 8 位区分
  mkdirSync(path.join(fixtureDir, "same-name-a"), { recursive: true });
  mkdirSync(path.join(fixtureDir, "same-name-b"), { recursive: true });
  writeFileSync(path.join(fixtureDir, "same-name-a", "同名.txt"), ["第一章 甲版本", "甲版本的正文内容，长度足够二十个非空白字符，用于占位。", ""].join("\n"), "utf8");
  writeFileSync(path.join(fixtureDir, "same-name-b", "同名.txt"), ["第一章 乙版本", "乙版本的正文内容，长度足够二十个非空白字符，用于占位。", ""].join("\n"), "utf8");
  // 修订脚本：行号区间重写边界 + 删除边界 + 标题覆盖
  writeFileSync(
    fixturePath("revisions.json"),
    JSON.stringify(
      {
        ops: [
          { op: "merge", line: 4 },
          { op: "range", from: 5, to: 11, boundaries: [{ line: 5, title: "第二章 乙续" }] },
          { op: "range", from: 7, to: 9, dropLines: [7] },
          { op: "rename", chapter: 3, title: "第三章 改名" },
        ],
        titleOverrides: { 1: "第一章 甲（覆盖）" },
      },
      null,
      2,
    ),
    "utf8",
  );
  writeFileSync(fixturePath("roman-revisions.json"), JSON.stringify({ ops: [{ op: "split", line: 3, title: "第XII章 罗马数字", level: "chapter" }] }, null, 2), "utf8");
});

after(() => {
  rmSync(tempRoot, { recursive: true, force: true });
});

describe("tool-split-chapters · 规范输入", () => {
  test("按标题行切章，卷边界与每章字数写入 manifest", { timeout: 20000 }, () => {
    const { manifest } = split("standard", ["--input", fixturePath("standard.txt"), "--reference-book-id", "demo-book", "--title", "测试书"]);

    assert.strictEqual(manifest.generator.id, "tool-split-chapters");
    assert.strictEqual(manifest.book.name, "测试书");
    assert.strictEqual(manifest.totalChapters, 6);
    assert.ok(manifest.totalChars > 0);
    assert.deepStrictEqual(manifest.volumes, [
      { no: 1, name: "第一卷 风起卷", from: 1, to: 3, assetId: "standard", chapterCount: 3 },
      { no: 2, name: "第二卷 江湖卷", from: 4, to: 6, assetId: "standard", chapterCount: 3 },
    ]);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), [
      "第一章 起点",
      "第二章 试炼",
      "第三章 下山",
      "第四章 初见",
      "第五章 交手",
      "第六章 归途",
    ]);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.volumeNo), [1, 1, 1, 2, 2, 2]);
    for (const chapter of manifest.chapters) {
      assert.ok(chapter.chars > 0);
      assert.match(chapter.file, /^ch\d{3}\.txt$/);
    }
    assert.strictEqual(manifest.agentArbitrationRequired, false);
    assert.deepStrictEqual(manifest.reasons, []);
    assert.strictEqual(manifest.confidence, 1);

    // 章文件落地：首行是标题行，正文非空
    const firstChapter = readFileSync(path.join(outDir("standard"), "chapters", "ch001.txt"), "utf8");
    assert.strictEqual(firstChapter.startsWith("第一章 起点\n"), true);
    assert.ok(firstChapter.includes("少年立于山巅"));
    assert.strictEqual(readdirSync(path.join(outDir("standard"), "chapters")).length, 6);

    // 章节索引：按资产的卷内序号
    const chapterIndex = readJson(path.join(outDir("standard"), "章节索引.json"));
    assert.strictEqual(chapterIndex.assets.length, 1);
    assert.strictEqual(chapterIndex.assets[0].chapterCount, 6);
    assert.deepStrictEqual(chapterIndex.assets[0].chapters.map((chapter) => chapter.volumeLocalNo), [1, 2, 3, 4, 5, 6]);

    // 合并章节索引：全书序号从 1 连续
    const merged = readJson(path.join(outDir("standard"), "合并章节索引.json"));
    assert.deepStrictEqual(merged.chapters.map((chapter) => chapter.globalNo), [1, 2, 3, 4, 5, 6]);
    assert.strictEqual(merged.chapters.every((chapter) => chapter.selected), true);
  });

  test("全角数字标题与 CRLF 归一后可识别，正文不残留 \\r", { timeout: 20000 }, () => {
    const { manifest } = split("crlf", ["--input", fixturePath("crlf.txt")]);
    assert.strictEqual(manifest.totalChapters, 2);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), ["第1章 全角风起", "第2章 全角雨落"]);
    const content = readFileSync(path.join(outDir("crlf"), "chapters", "ch001.txt"), "utf8");
    assert.strictEqual(content.includes("\r"), false);
  });

  test("dry-run 只计算不写盘", { timeout: 20000 }, () => {
    const target = outDir("dry-run");
    const result = runCli(["--input", fixturePath("standard.txt"), "--out", target, "--dry-run", "--json"]);
    assert.strictEqual(result.code, 0);
    assert.strictEqual(existsSync(target), false);
  });

  test("--scope chapters 只收窄批次计划与 selected 标记，不裁剪源包", { timeout: 20000 }, () => {
    const { manifest } = split("scope", ["--input", fixturePath("standard.txt"), "--scope", "chapters", "--from", "2", "--to", "3"]);
    assert.strictEqual(manifest.totalChapters, 6);
    assert.deepStrictEqual(manifest.scope, { type: "chapters", from: 2, to: 3, selectedChapters: 2, selectedVolumes: null });
    assert.deepStrictEqual(manifest.chapters.filter((chapter) => chapter.selected).map((chapter) => chapter.no), [2, 3]);
    assert.strictEqual(readdirSync(path.join(outDir("scope"), "chapters")).length, 6);
    const plan = readJson(path.join(outDir("scope"), "批次计划.json"));
    assert.strictEqual(plan.selectedChapters, 2);
    assert.strictEqual(plan.tiers.standard.totalChapters, 2);
  });
});

describe("tool-split-chapters · 编码识别", () => {
  test("GBK 输入按回退路径解码，标题与正文可读", { timeout: 20000 }, () => {
    const { manifest } = split("gbk", ["--input", fixturePath("gbk.txt")]);
    assert.strictEqual(manifest.encoding.primary, "gbk");
    assert.strictEqual(manifest.encoding.assets.gbk, "gbk");
    assert.strictEqual(manifest.encoding.methods.gbk, "fallback");
    assert.strictEqual(manifest.totalChapters, 3);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), ["第一章 风起", "第二章 雨落", "第三章 归途"]);
    const content = readFileSync(path.join(outDir("gbk"), "chapters", "ch001.txt"), "utf8");
    assert.ok(content.includes("少年立于山巅"));
    assert.strictEqual(content.includes("\uFFFD"), false);
  });
});

describe("tool-split-chapters · 低置信度与 Agent 裁决", () => {
  test("无标题行时输出单章、低置信度并标记需要裁决", { timeout: 20000 }, () => {
    const { manifest } = split("noheadings", ["--input", fixturePath("noheadings.txt")]);
    assert.strictEqual(manifest.totalChapters, 1);
    assert.strictEqual(manifest.agentArbitrationRequired, true);
    assert.ok(manifest.confidence < 0.6);
    assert.ok(manifest.reasons.length > 0);
    assert.ok(manifest.reasons.join("\n").includes("没有识别到章节标题"));
    assert.ok(manifest.chapters[0].flags.includes("no-boundary"));
  });

  test("未识别标题行占比超阈值触发裁决，回灌 revisions 后未识别标题清零；书本身的缺章仍留痕", { timeout: 30000 }, () => {
    const before = split("roman-before", ["--input", fixturePath("roman.txt")]);
    assert.strictEqual(before.manifest.agentArbitrationRequired, true);
    assert.strictEqual(before.manifest.quality.unrecognizedHeadings.length, 1);
    assert.ok(before.manifest.quality.unrecognizedHeadings[0].text.includes("第XII章"));
    assert.ok(before.manifest.reasons.join("\n").includes("未识别标题行占比"));

    const after = split("roman-after", ["--input", fixturePath("roman.txt"), "--revisions", fixturePath("roman-revisions.json")]);
    assert.strictEqual(after.manifest.totalChapters, 3);
    assert.deepStrictEqual(after.manifest.quality.unrecognizedHeadings, []);
    assert.ok(after.manifest.confidence > 0.9);
    assert.strictEqual(after.manifest.chapters[1].title, "第XII章 罗马数字");
    assert.strictEqual(after.manifest.revisionsApplied.some((item) => item.op === "split" && item.status === "applied"), true);
    // 边界问题解决了，但这本书本身缺第二章——缺号现在参与裁决，不再静默放行。
    assert.deepStrictEqual(after.manifest.quality.missing, [{ assetId: "roman", afterChapterNo: 1, missingNumbers: [2] }]);
    assert.strictEqual(after.manifest.agentArbitrationRequired, true);
    assert.ok(after.manifest.reasons.join("\n").includes("缺章号 1 个"));
  });

  test("重复章名与编号乱序触发裁决并写入 quality", { timeout: 20000 }, () => {
    const { manifest } = split("repeated", ["--input", fixturePath("repeated.txt")]);
    assert.strictEqual(manifest.totalChapters, 3);
    assert.strictEqual(manifest.quality.duplicated.length, 1);
    assert.strictEqual(manifest.quality.duplicated[0].title, "第三章 重逢");
    assert.deepStrictEqual(manifest.quality.duplicated[0].chapterNos, [2, 3]);
    assert.strictEqual(manifest.quality.outOfOrder.length, 1);
    assert.strictEqual(manifest.agentArbitrationRequired, true);
    assert.ok(manifest.reasons.join("\n").includes("重复章名"));
    assert.ok(manifest.reasons.join("\n").includes("编号乱序"));
    assert.ok(manifest.chapters[1].flags.includes("duplicated-title"));
  });
});

describe("tool-split-chapters · revisions", () => {
  test("按行号区间重写边界、删除边界并覆盖标题，全部记入 revisionsApplied", { timeout: 30000 }, () => {
    const baseline = split("revision-before", ["--input", fixturePath("revision-base.txt")]);
    assert.strictEqual(baseline.manifest.totalChapters, 4);

    const { manifest } = split("revision-after", ["--input", fixturePath("revision-base.txt"), "--revisions", fixturePath("revisions.json")]);
    assert.strictEqual(manifest.totalChapters, 3);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), ["第一章 甲（覆盖）", "第二章 乙续", "第三章 改名"]);
    assert.ok(manifest.chapters[1].flags.includes("revision-boundary"));
    assert.ok(manifest.chapters[2].flags.includes("revision-title"));
    assert.deepStrictEqual(manifest.quality.missing[0].missingNumbers, [2, 3]);

    const applied = manifest.revisionsApplied.filter((item) => item.status === "applied").map((item) => item.op);
    assert.ok(applied.includes("merge"));
    assert.ok(applied.includes("split"));
    assert.ok(applied.includes("rename"));
    assert.deepStrictEqual(manifest.revisionsApplied.filter((item) => item.status === "skipped"), []);

    // 章文件里的标题也跟着修订走
    const second = readFileSync(path.join(outDir("revision-after"), "chapters", "ch002.txt"), "utf8");
    assert.strictEqual(second.startsWith("第二章 乙续\n"), true);
  });

  test("同输入同参数两次运行，除 generatedAt 外产物一致", { timeout: 30000 }, () => {
    const first = split("repro-a", ["--input", fixturePath("standard.txt"), "--input", fixturePath("vol2.txt")]);
    const second = split("repro-b", ["--input", fixturePath("standard.txt"), "--input", fixturePath("vol2.txt")]);
    const firstMerged = readFileSync(path.join(outDir("repro-a"), "合并章节索引.json"), "utf8");
    const secondMerged = readFileSync(path.join(outDir("repro-b"), "合并章节索引.json"), "utf8");
    assert.strictEqual(JSON.stringify(first.manifest.chapters), JSON.stringify(second.manifest.chapters));
    assert.strictEqual(firstMerged.split("\n").slice(2).join("\n"), secondMerged.split("\n").slice(2).join("\n"));
  });
});

describe("tool-split-chapters · 范围校验", () => {
  test("6 章输入要前 10 章被拒绝，且不写出任何产物", { timeout: 20000 }, () => {
    const target = outDir("reject");
    const result = runCli(["--input", fixturePath("standard.txt"), "--out", target, "--scope", "chapters", "--from", "1", "--to", "10"]);
    assert.notStrictEqual(result.code, 0);
    assert.strictEqual(result.code, 2);
    assert.ok(result.stderr.includes("范围校验失败"));
    assert.ok(result.stderr.includes("共 6 章"));
    assert.ok(result.stderr.includes("1-10"));
    assert.strictEqual(existsSync(target), false);
  });

  test("--scope volume 越界同样被拒绝", { timeout: 20000 }, () => {
    const target = outDir("reject-volume");
    const result = runCli(["--input", fixturePath("standard.txt"), "--out", target, "--scope", "volume", "--from", "1", "--to", "3"]);
    assert.strictEqual(result.code, 2);
    assert.ok(result.stderr.includes("范围校验失败"));
    assert.ok(result.stderr.includes("共 2 卷"));
    assert.strictEqual(existsSync(target), false);
  });
});

describe("tool-split-chapters · 多资产", () => {
  test("多资产按序拼接，全书序号连续、卷内序号重置、assetId 可追溯", { timeout: 20000 }, () => {
    const { manifest } = split("multi", ["--input", fixturePath("vol1.txt"), "--input", fixturePath("vol2.txt"), "--reference-book-id", "multi-book", "--title", "多卷书"]);

    assert.strictEqual(manifest.totalChapters, 5);
    assert.deepStrictEqual(manifest.book.source, ["vol1.txt", "vol2.txt"]);
    assert.deepStrictEqual(manifest.volumes.map((volume) => ({ no: volume.no, name: volume.name, from: volume.from, to: volume.to })), [
      { no: 1, name: "vol1", from: 1, to: 3 },
      { no: 2, name: "vol2", from: 4, to: 5 },
    ]);

    const merged = readJson(path.join(outDir("multi"), "合并章节索引.json"));
    assert.deepStrictEqual(merged.chapters.map((chapter) => chapter.globalNo), [1, 2, 3, 4, 5]);
    assert.deepStrictEqual(merged.chapters.map((chapter) => chapter.volumeLocalNo), [1, 2, 3, 1, 2]);
    assert.deepStrictEqual(merged.chapters.map((chapter) => chapter.assetId), ["vol1", "vol1", "vol1", "vol2", "vol2"]);
    assert.deepStrictEqual(merged.chapters.map((chapter) => chapter.volumeNo), [1, 1, 1, 2, 2]);

    const chapterIndex = readJson(path.join(outDir("multi"), "章节索引.json"));
    assert.deepStrictEqual(chapterIndex.assets.map((asset) => [asset.assetId, asset.chapterCount]), [
      ["vol1", 3],
      ["vol2", 2],
    ]);
  });

  test("相同指纹的资产被去重，只算一次章，后 8 位与 sha256 一致", { timeout: 20000 }, () => {
    const { manifest } = split("dedup", ["--input", fixturePath("dupA.txt"), "--input", fixturePath("dupB-副本.txt")]);
    assert.strictEqual(manifest.totalChapters, 2);
    assert.strictEqual(manifest.duplicates.length, 1);
    assert.strictEqual(manifest.duplicates[0].duplicateOf, "dupA");
    assert.strictEqual(manifest.ignoredInputs.length, 1);

    const fingerprints = readJson(path.join(outDir("dedup"), "指纹.json"));
    assert.strictEqual(fingerprints.algorithm, "sha256");
    assert.strictEqual(fingerprints.shortHashLength, 8);
    assert.strictEqual(fingerprints.assets.length, 2);
    for (const asset of fingerprints.assets) {
      assert.strictEqual(asset.shortHash, asset.sha256.slice(-8));
    }
    assert.strictEqual(fingerprints.assets[0].duplicateOf, null);
    assert.strictEqual(fingerprints.assets[1].duplicateOf, "dupA");
    assert.strictEqual(fingerprints.assets[1].sha256, fingerprints.assets[0].sha256);
    assert.strictEqual(fingerprints.duplicateGroups.length, 1);
    assert.deepStrictEqual(fingerprints.duplicateGroups[0].assetIds, ["dupA", "dupB-副本"]);
    assert.strictEqual(fingerprints.uniqueCount, 1);
  });

  test("同名不同文件用指纹后 8 位区分，合并索引里各自可寻址", { timeout: 20000 }, () => {
    const { manifest } = split("same-name", [
      "--input",
      path.join(fixtureDir, "same-name-a", "同名.txt"),
      "--input",
      path.join(fixtureDir, "same-name-b", "同名.txt"),
    ]);

    assert.strictEqual(manifest.totalChapters, 2);
    assert.strictEqual(manifest.volumes.length, 2);
    const [firstAssetId, secondAssetId] = manifest.volumes.map((volume) => volume.assetId);
    assert.strictEqual(firstAssetId, "同名");
    assert.match(secondAssetId, /^同名~[0-9a-f]{8}$/);
    const fingerprints = readJson(path.join(outDir("same-name"), "指纹.json"));
    const second = fingerprints.assets.find((asset) => asset.assetId === secondAssetId);
    assert.strictEqual(second?.shortHash, secondAssetId.split("~")[1]);
  });
});

describe("tool-split-chapters · 批次计划", () => {
  test("三档切批口径：standard ≤30、deep ≤20、outline ≤40，档位键名即交付物名", { timeout: 30000 }, () => {
    const { manifest } = split("batches", ["--input", fixturePath("many.txt")]);
    assert.strictEqual(manifest.totalChapters, 45);

    const plan = readJson(path.join(outDir("batches"), "批次计划.json"));
    assert.strictEqual(plan.profile, "standard");
    assert.strictEqual(plan.activeTier, "standard");
    assert.strictEqual(plan.activeTierLabel, "标准档");
    assert.deepStrictEqual(plan.batches, plan.tiers.standard.batches);

    // 档位键名固定为 standard / deep / outline 三档；旧名 quality / skeleton 不得再出现
    assert.deepStrictEqual(Object.keys(plan.tiers).sort(), ["deep", "outline", "standard"]);
    assert.strictEqual(Object.keys(plan.tiers).every((key) => ["standard", "deep", "outline"].includes(key)), true);
    assert.strictEqual(JSON.stringify(plan).includes("quality"), false);
    assert.strictEqual(JSON.stringify(plan).includes("skeleton"), false);
    // 脚本里也必须彻底删掉旧档位名，避免两套叫法
    const scriptSource = readFileSync(SCRIPT_PATH, "utf8");
    assert.strictEqual(scriptSource.includes("skeleton"), false);
    assert.strictEqual(scriptSource.includes('"quality"'), false);

    assert.strictEqual(plan.tiers.standard.batchSize, 30);
    assert.strictEqual(plan.tiers.standard.batchCount, 2);
    assert.deepStrictEqual(plan.tiers.standard.batches.map((batch) => batch.chapterCount), [30, 15]);
    assert.strictEqual(plan.tiers.deep.batchSize, 20);
    assert.strictEqual(plan.tiers.deep.batchCount, 3);
    assert.deepStrictEqual(plan.tiers.deep.batches.map((batch) => batch.chapterCount), [20, 20, 5]);
    assert.strictEqual(plan.tiers.outline.batchSize, 40);
    assert.strictEqual(plan.tiers.outline.batchCount, 2);
    assert.deepStrictEqual(plan.tiers.outline.batches.map((batch) => batch.chapterCount), [40, 5]);

    for (const tier of Object.values(plan.tiers)) {
      assert.strictEqual(tier.totalChapters, 45);
      // 任何档位每批不超过 40 章
      assert.ok(tier.batchSize <= 40);
      for (const batch of tier.batches) {
        assert.ok(batch.chapterCount <= tier.batchSize);
        assert.strictEqual(batch.toGlobalNo - batch.fromGlobalNo + 1, batch.chapterCount);
        assert.strictEqual(batch.files.length, batch.chapterCount);
        for (const file of batch.files) {
          assert.match(file, /^ch\d{3}\.txt$/);
        }
      }
      // 批次必须连续覆盖全部选中章，且文件清单与 manifest 章清单一致
      assert.strictEqual(tier.batches[0].fromGlobalNo, 1);
      assert.strictEqual(tier.batches[tier.batches.length - 1].toGlobalNo, 45);
      for (let i = 1; i < tier.batches.length; i += 1) {
        assert.strictEqual(tier.batches[i].fromGlobalNo, tier.batches[i - 1].toGlobalNo + 1);
      }
      assert.deepStrictEqual(tier.batches.flatMap((batch) => batch.files), manifest.chapters.map((chapter) => chapter.file));
    }
  });

  test("--profile deep 走深度档（六模块完整交付、质量优先），每批 ≤20 章", { timeout: 30000 }, () => {
    const { manifest } = split("batches-deep", ["--input", fixturePath("many.txt"), "--profile", "deep"]);
    assert.strictEqual(manifest.activeTier, "deep");
    const plan = readJson(path.join(outDir("batches-deep"), "批次计划.json"));
    assert.strictEqual(plan.profile, "deep");
    assert.strictEqual(plan.activeTier, "deep");
    assert.strictEqual(plan.activeTierLabel, "深度档");
    assert.deepStrictEqual(plan.batches, plan.tiers.deep.batches);
    assert.strictEqual(plan.tiers.deep.batchSize, 20);
    assert.deepStrictEqual(plan.tiers.deep.batches.map((batch) => batch.chapterCount), [20, 20, 5]);
    // 三档结果始终同时给出
    assert.deepStrictEqual(Object.keys(plan.tiers).sort(), ["deep", "outline", "standard"]);
  });

  test("--profile outline 走骨架档（卷级骨架，另一种交付物），每批 ≤40 章", { timeout: 30000 }, () => {
    const { manifest } = split("batches-outline", ["--input", fixturePath("many.txt"), "--profile", "outline"]);
    assert.strictEqual(manifest.activeTier, "outline");
    const plan = readJson(path.join(outDir("batches-outline"), "批次计划.json"));
    assert.strictEqual(plan.profile, "outline");
    assert.strictEqual(plan.activeTier, "outline");
    assert.strictEqual(plan.activeTierLabel, "骨架档");
    assert.deepStrictEqual(plan.batches, plan.tiers.outline.batches);
    assert.strictEqual(plan.tiers.outline.batchSize, 40);
    assert.deepStrictEqual(plan.tiers.outline.batches.map((batch) => batch.chapterCount), [40, 5]);
    assert.deepStrictEqual(Object.keys(plan.tiers).sort(), ["deep", "outline", "standard"]);
  });
});

describe("tool-split-chapters · 真实网文 TXT 排版", () => {
  test("《道诡异仙》式 Markdown 排版：#{1,6} 标题、加粗标题、非章标题、分隔符、内部卷标记都能正确识别", { timeout: 30000 }, () => {
    const { manifest } = split("mdbook", ["--input", fixturePath("mdbook.txt")]);

    // 1072 条 Markdown 标题式的排版：带章节号的才是章，一行都不多、一行都不少
    assert.strictEqual(manifest.totalChapters, 4);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), ["第一章 师傅", "第二章 雨落", "第三章 夜行", "第四章 收尾"]);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.number), [1, 2, 3, 4]);

    // 不含章节号的 Markdown 标题（作者的话 / 番外）登记为非章标题，不建边界、不打断编号
    assert.deepStrictEqual(manifest.nonChapterHeadings, [
      { assetId: "mdbook", line: 5, title: "上架感言", type: "author-note" },
      { assetId: "mdbook", line: 14, title: "番外：清旺来", type: "side-story" },
    ]);

    // 非章标题的正文归入上一章，并给该章打 flag
    const first = manifest.chapters[0];
    const third = manifest.chapters[2];
    assert.ok(first.flags.includes("contains-non-chapter-heading"));
    assert.ok(third.flags.includes("contains-non-chapter-heading"));
    assert.strictEqual(manifest.chapters[1].flags.includes("contains-non-chapter-heading"), false);
    assert.strictEqual(manifest.chapters[3].flags.includes("contains-non-chapter-heading"), false);
    const firstFile = readFileSync(path.join(outDir("mdbook"), "chapters", "ch001.txt"), "utf8");
    assert.strictEqual(firstFile.startsWith("第一章 师傅\n"), true);
    assert.ok(firstFile.includes("上架感言"));
    assert.ok(firstFile.includes("明天就要上架了"));

    // 加粗包裹（**第X章 xx**）派生出的标题不带星号
    const thirdFile = readFileSync(path.join(outDir("mdbook"), "chapters", "ch003.txt"), "utf8");
    assert.strictEqual(thirdFile.startsWith("第三章 夜行\n"), true);
    assert.strictEqual(thirdFile.includes("**"), false);

    // 内部卷标记只登记，不改「一个资产 = 一卷」
    assert.deepStrictEqual(manifest.volumeMarkers, [{ assetId: "mdbook", line: 22, name: "第一卷", complete: true }]);
    assert.deepStrictEqual(manifest.meta.internalVolumeAssets, ["mdbook"]);
    assert.deepStrictEqual(manifest.volumes, [{ no: 1, name: "mdbook", from: 1, to: 4, assetId: "mdbook", chapterCount: 4 }]);

    // `******` 这类分隔符不是标题，也不进非章标题清单
    assert.strictEqual(manifest.chapters.every((chapter) => !chapter.title.includes("*")), true);
    assert.strictEqual(manifest.nonChapterHeadings.every((heading) => !heading.title.includes("*")), true);

    // 编号 1-4 连续、无缺号/重号/乱序、无未识别标题行 -> 置信度 1，不需要裁决
    assert.deepStrictEqual(manifest.quality.missing, []);
    assert.deepStrictEqual(manifest.quality.duplicated, []);
    assert.deepStrictEqual(manifest.quality.outOfOrder, []);
    assert.deepStrictEqual(manifest.quality.unrecognizedHeadings, []);
    assert.strictEqual(manifest.confidence, 1);
    assert.strictEqual(manifest.agentArbitrationRequired, false);
    assert.deepStrictEqual(manifest.reasons, []);
  });

  test("混合两种来源 + 重号 + 缺号 + 盗版残留：清理标题后缀但保留证据，正常标题文字不被误删", { timeout: 30000 }, () => {
    const { manifest } = split("mixedbook", ["--input", fixturePath("mixedbook.txt")]);

    // Markdown 标题与裸标题混排：两处「第一百二十章」都被切出来（重号），且没有多切
    assert.strictEqual(manifest.totalChapters, 5);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), [
      "第一章 师傅",
      "第一百二十章 伤口",
      "第一百二十章 伤口",
      "第一百二十二章 赶路",
      "第一百二十三章 免费阅读的秘密",
    ]);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.number), [1, 120, 120, 122, 123]);

    // 盗版站残留：标题派生时清掉「免费阅读」与尾部标点，证据留在 flags
    const residueChapter = manifest.chapters[2];
    assert.ok(residueChapter.flags.includes("title-residue:免费阅读"));
    assert.strictEqual(residueChapter.title, "第一百二十章 伤口");
    assert.strictEqual(residueChapter.flags.includes("contamination"), false);

    // 正常标题里的同样字眼不能被误删
    const cleanChapter = manifest.chapters[4];
    assert.strictEqual(cleanChapter.title, "第一百二十三章 免费阅读的秘密");
    assert.strictEqual(cleanChapter.flags.some((flag) => flag.startsWith("title-residue")), false);

    // 重号 / 缺号 / 乱序都写进 quality
    assert.strictEqual(manifest.quality.duplicated.length, 1);
    assert.strictEqual(manifest.quality.duplicated[0].assetId, "mixedbook");
    assert.strictEqual(manifest.quality.duplicated[0].title, "第一百二十章 伤口");
    assert.deepStrictEqual(manifest.quality.duplicated[0].chapterNos, [2, 3]);
    // 缺号一律留痕：1 → 120 的超大缺口现在也会记录（列表截断到 50 个），不再被旧的 50 上限吞掉
    assert.strictEqual(manifest.quality.missing.length, 2);
    assert.strictEqual(manifest.quality.missing[0].assetId, "mixedbook");
    assert.strictEqual(manifest.quality.missing[0].afterChapterNo, 1);
    assert.strictEqual(manifest.quality.missing[0].missingNumbers.length, 50);
    assert.deepStrictEqual(manifest.quality.missing[1], { assetId: "mixedbook", afterChapterNo: 3, missingNumbers: [121] });
    assert.strictEqual(manifest.quality.outOfOrder.length, 1);
    assert.ok(manifest.chapters[1].flags.includes("duplicated-title"));
    assert.ok(manifest.chapters[2].flags.includes("out-of-order"));
    assert.strictEqual(manifest.confidence, 0.9);
    assert.strictEqual(manifest.agentArbitrationRequired, true);
    assert.ok(manifest.reasons.join("\n").includes("重复章名"));
    assert.ok(manifest.reasons.join("\n").includes("编号乱序"));

    // 非章 Markdown 标题仍不建边界、正文归入上一章；内部卷标记仍不建卷边界
    assert.deepStrictEqual(manifest.nonChapterHeadings, [{ assetId: "mixedbook", line: 16, title: "抱歉", type: "author-note" }]);
    assert.ok(manifest.chapters[4].flags.includes("contains-non-chapter-heading"));
    assert.strictEqual(manifest.chapters[4].lineStart, 13);
    assert.deepStrictEqual(manifest.chapters.filter((chapter) => chapter.flags.includes("contains-non-chapter-heading")).map((chapter) => chapter.no), [5]);
    assert.deepStrictEqual(manifest.volumeMarkers, [{ assetId: "mixedbook", line: 21, name: "第二卷", complete: true }]);
    assert.deepStrictEqual(manifest.meta.internalVolumeAssets, ["mixedbook"]);
    assert.strictEqual(manifest.volumes.length, 1);
    assert.strictEqual(manifest.volumes[0].name, "mixedbook");
  });

  test("作者公告里的「1、2、4、5、」编号清单不会被当成章（有强章边界时不再采纳弱式数字标题）", { timeout: 30000 }, () => {
    const { manifest } = split("notelist", ["--input", fixturePath("notelist.txt")]);
    assert.strictEqual(manifest.totalChapters, 2);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), ["第一章 师傅", "第二章 雨落"]);
    assert.strictEqual(manifest.chapters.every((chapter) => !chapter.weakTitle), true);
    assert.strictEqual(manifest.meta.numberedHeadingsAdopted.notelist, false);

    // 公告是非章标题，清单只是它的正文，整段归入上一章
    assert.deepStrictEqual(manifest.nonChapterHeadings, [{ assetId: "notelist", line: 3, title: "关于抖音直播", type: "author-note" }]);
    assert.ok(manifest.chapters[0].flags.includes("contains-non-chapter-heading"));
    assert.strictEqual(manifest.chapters[0].lineStart, 1);
    assert.deepStrictEqual(manifest.chapters.filter((chapter) => chapter.flags.includes("contains-non-chapter-heading")).map((chapter) => chapter.no), [1]);
    const firstFile = readFileSync(path.join(outDir("notelist"), "chapters", "ch001.txt"), "utf8");
    assert.ok(firstFile.includes("1、关注这《道诡异仙》抖音账号"));
    assert.ok(firstFile.includes("5、奖励上限者不再进行补发。"));

    assert.deepStrictEqual(manifest.quality.outOfOrder, []);
    assert.strictEqual(manifest.agentArbitrationRequired, false);
    assert.strictEqual(manifest.confidence, 1);
  });

  test("作者感言「第二卷写完了…」不被当成卷边界，也不会变成章，只作为疑似标题行交给 Agent 裁决", { timeout: 30000 }, () => {
    const { manifest } = split("volremark", ["--input", fixturePath("volremark.txt")]);
    assert.strictEqual(manifest.totalChapters, 2);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), ["第一章 甲", "第二章 乙"]);
    // 不建卷边界、不记内部卷标记，仍然只有一个资产卷
    assert.deepStrictEqual(manifest.volumeMarkers, []);
    assert.deepStrictEqual(manifest.meta.internalVolumeAssets, []);
    assert.strictEqual(manifest.volumes.length, 1);
    assert.strictEqual(manifest.volumes[0].name, "volremark");
    // 这句感言被当成疑似标题行暴露出来，等 Agent 裁
    assert.deepStrictEqual(manifest.quality.unrecognizedHeadings.map((item) => item.text), ["第二卷写完了，嗯…那我就歇一天吧。还望各位见谅"]);
    assert.strictEqual(manifest.agentArbitrationRequired, true);
    assert.ok(manifest.reasons.join("\n").includes("未识别标题行占比"));
  });
});

describe("tool-split-chapters · 跨资产对齐（正文台账快照）", () => {
  test("干净续接：per-asset 章号区间与 continues 关系都写进 manifest.crossAsset", { timeout: 20000 }, () => {
    const { manifest } = split("cross-continues", ["--input", fixturePath("vol1.txt"), "--input", fixturePath("vol2.txt")]);
    const { assets, relations } = manifest.crossAsset;

    // 每个上传文件 → 本书内 xx-xx 章
    assert.deepStrictEqual(assets.map((asset) => [asset.assetId, asset.fromGlobalNo, asset.toGlobalNo, asset.chapterCount]), [
      ["vol1", 1, 3, 3],
      ["vol2", 4, 5, 2],
    ]);
    assert.deepStrictEqual(assets.map((asset) => [asset.firstNumber, asset.lastNumber]), [[1, 3], [4, 5]]);
    assert.deepStrictEqual(assets.map((asset) => asset.fileName), ["vol1.txt", "vol2.txt"]);
    assert.deepStrictEqual(assets.map((asset) => asset.volumeNos), [[1], [2]]);

    assert.deepStrictEqual(relations.map((relation) => relation.kind), ["first", "continues"]);
    assert.strictEqual(relations[1].previousAssetId, "vol1");
    assert.strictEqual(relations[1].previousLastNumber, 3);
    assert.strictEqual(relations[1].currentFirstNumber, 4);
    assert.strictEqual(relations[1].overlapChapters, 0);
    // 干净续接不该触发裁决，也不产生任何跨资产扣分
    assert.strictEqual(manifest.agentArbitrationRequired, false);
    assert.strictEqual(manifest.confidenceSignals.crossAssetOverlaps, 0);
    assert.strictEqual(manifest.confidenceSignals.crossAssetDuplicateTitles, 0);
    assert.strictEqual(manifest.confidenceSignals.crossAssetRestarts, 0);
  });

  test("编号重叠：记为 overlaps 并触发裁决，说明是哪两卷重叠多少章", { timeout: 20000 }, () => {
    // vol1 = 第一章..第三章，overlap = 第二章..第三章 -> 本卷首号 2 ≤ 上卷末号 3
    const { manifest } = split("cross-overlaps", ["--input", fixturePath("vol1.txt"), "--input", fixturePath("overlap.txt")]);
    assert.deepStrictEqual(manifest.crossAsset.relations.map((relation) => relation.kind), ["first", "overlaps"]);
    const relation = manifest.crossAsset.relations[1];
    assert.strictEqual(relation.previousAssetId, "vol1");
    assert.strictEqual(relation.previousLastNumber, 3);
    assert.strictEqual(relation.currentFirstNumber, 2);
    assert.strictEqual(relation.overlapChapters, 2);
    assert.strictEqual(manifest.confidenceSignals.crossAssetOverlaps, 1);
    assert.strictEqual(manifest.agentArbitrationRequired, true);
    assert.ok(manifest.reasons.join("\n").includes("跨卷章节编号重叠"));
    assert.ok(manifest.reasons.join("\n").includes("需判定是否为重复上传的同一卷"));
  });

  test("每卷从第一章重新编号：记为 restarts，属常见排版，不触发裁决", { timeout: 20000 }, () => {
    const { manifest } = split("cross-restarts", ["--input", fixturePath("vol1.txt"), "--input", fixturePath("restart.txt")]);
    assert.deepStrictEqual(manifest.crossAsset.relations.map((relation) => relation.kind), ["first", "restarts"]);
    const relation = manifest.crossAsset.relations[1];
    assert.strictEqual(relation.currentFirstNumber, 1);
    assert.strictEqual(relation.overlapChapters, 0);
    // 重置编号不是问题：既不触发裁决，也不产生跨资产扣分
    assert.strictEqual(manifest.confidenceSignals.crossAssetRestarts, 1);
    assert.strictEqual(manifest.confidenceSignals.crossAssetOverlaps, 0);
    assert.strictEqual(manifest.agentArbitrationRequired, false);
  });

  test("跨卷重复章名：记为 crossAsset.duplicates 并触发裁决", { timeout: 30000 }, () => {
    const { manifest } = split("cross-duplicates", ["--input", fixturePath("same-title-a.txt"), "--input", fixturePath("same-title-b.txt")]);
    assert.strictEqual(manifest.crossAsset.duplicates.length, 1);
    const duplicate = manifest.crossAsset.duplicates[0];
    assert.strictEqual(duplicate.title, "第一章 同题");
    assert.deepStrictEqual(duplicate.assetIds, ["same-title-a", "same-title-b"]);
    assert.strictEqual(duplicate.occurrenceCount, 2);
    assert.strictEqual(duplicate.sameNumber, true);
    assert.strictEqual(manifest.agentArbitrationRequired, true);
    assert.ok(manifest.reasons.join("\n").includes("跨卷重复章名"));

    // 单资产时不存在跨卷关系与跨卷重名
    const single = split("cross-single", ["--input", fixturePath("vol1.txt")]);
    assert.deepStrictEqual(single.manifest.crossAsset.relations.map((relation) => relation.kind), ["first"]);
    assert.deepStrictEqual(single.manifest.crossAsset.duplicates, []);
    assert.strictEqual(single.manifest.agentArbitrationRequired, false);
  });

  test("同样落进 stdout 摘要，宿主无需另读文件即可拿到台账快照", { timeout: 20000 }, () => {
    const { summary } = split("cross-summary", ["--input", fixturePath("vol1.txt"), "--input", fixturePath("vol2.txt")]);
    assert.strictEqual(Array.isArray(summary.sources), true);
    assert.deepStrictEqual(summary.sources.map((item) => [item.assetId, item.fromGlobalNo, item.toGlobalNo]), [
      ["vol1", 1, 3],
      ["vol2", 4, 5],
    ]);
    assert.strictEqual(summary.crossAsset.overlaps, 0);
    assert.strictEqual(summary.crossAsset.duplicateTitles, 0);
    assert.strictEqual(summary.crossAsset.restarts, 0);
    assert.strictEqual(summary.crossAsset.gaps, 0);
  });
});

describe("tool-split-chapters · 源清洗", () => {
  test("默认只给预览、不改盘：清洗计数照出，章节仍按原文切", { timeout: 30000 }, () => {
    const { manifest, summary } = split("clean-preview", ["--input", fixturePath("cleaning.txt")]);
    const cleaning = summary.cleaning;
    assert.strictEqual(cleaning.applied, false);
    assert.strictEqual(cleaning.removedLines, 5);
    assert.strictEqual(cleaning.removedByRule["error-overlay"], 4);
    assert.strictEqual(cleaning.removedByRule["url-only"], 1);
    assert.strictEqual(cleaning.mergedPageDuplicates, 1);
    assert.strictEqual(cleaning.trimmedLines, 1);
    assert.strictEqual(cleaning.suspicion.length, 1);
    assert.strictEqual(cleaning.cleanedTextHash, null);
    // 预览不改盘：分页重复标题还在，所以仍是 4 章
    assert.strictEqual(manifest.totalChapters, 4);
    assert.strictEqual(manifest.cleaning.applied, false);
  });

  test("--clean 删整行噪声、合并分页重复标题、剥掉标题上的分页标记，且不动正文里的噪声词", { timeout: 30000 }, () => {
    const { manifest } = split("clean-apply", ["--input", fixturePath("cleaning.txt"), "--clean"]);
    assert.strictEqual(manifest.cleaning.applied, true);
    assert.strictEqual(manifest.cleaning.removedByRule["error-overlay"], 4);
    assert.strictEqual(manifest.cleaning.removedByRule["url-only"], 1);
    assert.strictEqual(manifest.cleaning.mergedPageDuplicates, 1);
    assert.strictEqual(manifest.cleaning.suspicion.length, 1);

    assert.strictEqual(manifest.totalChapters, 3);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), ["第一章 风起", "第二章 雨落", "第三章 归途"]);
    assert.deepStrictEqual(manifest.quality.outOfOrder, []);
    assert.deepStrictEqual(manifest.quality.missing, []);

    const second = readFileSync(path.join(outDir("clean-apply"), "chapters", "ch002.txt"), "utf8");
    // 正文里含「最新章节」的句子保留（residue 门挡住），噪声行不进正文
    assert.ok(second.includes("这本要收费才能看最新章节"));
    assert.strictEqual(second.includes("请选择错误类型"), false);
    assert.strictEqual(second.includes("pirate-site.com"), false);
  });

  test("--clean 剔除「后文以标题+正文再次出现」的目录块，缩掉由目录造成的假乱序", { timeout: 30000 }, () => {
    const preview = split("clean-toc-preview", ["--input", fixturePath("cleaning-toc.txt")]);
    assert.strictEqual(preview.manifest.totalChapters, 6);
    assert.strictEqual(preview.manifest.cleaning.droppedTocLines, 3);
    assert.strictEqual(preview.manifest.cleaning.droppedTocBlocks, 1);

    const { manifest } = split("clean-toc", ["--input", fixturePath("cleaning-toc.txt"), "--clean"]);
    assert.strictEqual(manifest.totalChapters, 3);
    assert.strictEqual(manifest.cleaning.droppedTocLines, 3);
    assert.deepStrictEqual(manifest.chapters.map((chapter) => chapter.title), ["第001章 风起", "第002章 雨落", "第003章 归途"]);
    assert.deepStrictEqual(manifest.quality.outOfOrder, []);
    assert.strictEqual(manifest.agentArbitrationRequired, false);
  });

  test("干净源零改动：--clean 对规范输入不删任何行", { timeout: 30000 }, () => {
    const { manifest } = split("clean-noop", ["--input", fixturePath("standard.txt"), "--clean"]);
    assert.strictEqual(manifest.cleaning.applied, true);
    assert.strictEqual(manifest.cleaning.removedLines, 0);
    assert.strictEqual(manifest.cleaning.trimmedLines, 0);
    assert.strictEqual(manifest.cleaning.mergedPageDuplicates, 0);
    assert.deepStrictEqual(manifest.cleaning.suspicion, []);
    assert.strictEqual(manifest.totalChapters, 6);
    assert.strictEqual(manifest.confidence, 1);
  });

  test("幂等：同一输入两次 --clean，章节与清洗指纹一致", { timeout: 30000 }, () => {
    const first = split("clean-idem-a", ["--input", fixturePath("cleaning.txt"), "--clean"]);
    const second = split("clean-idem-b", ["--input", fixturePath("cleaning.txt"), "--clean"]);
    assert.strictEqual(JSON.stringify(first.manifest.chapters), JSON.stringify(second.manifest.chapters));
    assert.strictEqual(first.manifest.cleaning.cleanedTextHash, second.manifest.cleaning.cleanedTextHash);
  });

  test("--clean-out 把清洗后的完整正文写到 <dir>/0.txt，且不影响既有产物", { timeout: 30000 }, () => {
    const cleanRoot = mkdtempSync(path.join(os.tmpdir(), "popwave-clean-out-"));
    try {
      // 目录故意不预先创建：验证递归创建
      const cleanDir = path.join(cleanRoot, "cleaned");
      const baseline = split("clean-out-baseline", ["--input", fixturePath("cleaning.txt"), "--clean"]);
      const { manifest } = split("clean-out", ["--input", fixturePath("cleaning.txt"), "--clean", "--clean-out", cleanDir]);

      const cleanedFile = path.join(cleanDir, "0.txt");
      assert.strictEqual(existsSync(cleanedFile), true);
      const content = readFileSync(cleanedFile, "utf8");

      // 对照 manifest.cleaning.removedByRule 里删掉的那几条：浮层文案与纯网址行都不该出现
      assert.strictEqual(manifest.cleaning.removedByRule["error-overlay"], 4);
      assert.strictEqual(manifest.cleaning.removedByRule["url-only"], 1);
      assert.strictEqual(content.includes("请选择错误类型"), false);
      assert.strictEqual(content.includes("更新太慢"), false);
      assert.strictEqual(content.includes("缺少章节"), false);
      assert.strictEqual(content.includes("章节内容错误"), false);
      assert.strictEqual(content.includes("www.pirate-site.com"), false);

      // 以正文章节开头（首行是第一章标题，而非浮层噪声）
      assert.strictEqual(content.startsWith("第一章 风起"), true);
      assert.match(content, /^第[0-9一二三四五六七八九十百千万]+章\s/);

      // 新选项不影响既有产物：chapters/ 与 manifest 都与不带 --clean-out 时一致
      assert.strictEqual(JSON.stringify(manifest.chapters), JSON.stringify(baseline.manifest.chapters));
      const baselineChapters = readdirSync(path.join(outDir("clean-out-baseline"), "chapters")).sort();
      const withOutChapters = readdirSync(path.join(outDir("clean-out"), "chapters")).sort();
      assert.deepStrictEqual(withOutChapters, baselineChapters);
      for (const file of withOutChapters) {
        assert.strictEqual(readFileSync(path.join(outDir("clean-out"), "chapters", file), "utf8"), readFileSync(path.join(outDir("clean-out-baseline"), "chapters", file), "utf8"));
      }
    } finally {
      rmSync(cleanRoot, { recursive: true, force: true });
    }
  });

  test("--clean-out 只在 --clean 时有效：缺 --clean 退出码 2 且不写任何文件", { timeout: 30000 }, () => {
    const cleanRoot = mkdtempSync(path.join(os.tmpdir(), "popwave-clean-out-gate-"));
    try {
      const cleanDir = path.join(cleanRoot, "cleaned");
      mkdirSync(cleanDir, { recursive: true });
      const target = outDir("clean-out-no-clean");
      const result = runCli(["--input", fixturePath("cleaning.txt"), "--out", target, "--clean-out", cleanDir]);
      assert.strictEqual(result.code, 2);
      assert.ok(result.stderr.includes("--clean-out 只在 --clean 时有效，请同时加上 --clean"));
      assert.deepStrictEqual(readdirSync(cleanDir), []);
      assert.strictEqual(existsSync(target), false);
    } finally {
      rmSync(cleanRoot, { recursive: true, force: true });
    }
  });

  test("--dry-run 与 --clean-out 互斥：退出码 2 且不写盘", { timeout: 30000 }, () => {
    const cleanRoot = mkdtempSync(path.join(os.tmpdir(), "popwave-clean-out-dry-"));
    try {
      const cleanDir = path.join(cleanRoot, "cleaned");
      mkdirSync(cleanDir, { recursive: true });
      const result = runCli(["--input", fixturePath("cleaning.txt"), "--dry-run", "--clean", "--clean-out", cleanDir]);
      assert.strictEqual(result.code, 2);
      assert.ok(result.stderr.includes("--dry-run 与 --clean-out 不能同时使用"));
      assert.deepStrictEqual(readdirSync(cleanDir), []);
    } finally {
      rmSync(cleanRoot, { recursive: true, force: true });
    }
  });

  test("清洗不改指纹：指纹仍按原上传文件算，清洗后文本另记 cleanedTextHash", { timeout: 30000 }, () => {
    const { manifest } = split("clean-fingerprint", ["--input", fixturePath("cleaning.txt"), "--clean"]);
    const fingerprints = readJson(path.join(outDir("clean-fingerprint"), "指纹.json"));
    assert.match(fingerprints.assets[0].sha256, /^[0-9a-f]{64}$/);
    assert.match(fingerprints.assets[0].cleanedTextHash, /^[0-9a-f]{64}$/);
    assert.notStrictEqual(fingerprints.assets[0].cleanedTextHash, fingerprints.assets[0].sha256);
    assert.match(manifest.cleaning.cleanedTextHash, /^[0-9a-f]{64}$/);
  });
});

describe("tool-split-chapters · 脚本自检", () => {
  test("脚本目录与 skill 清单齐备，且脚本零第三方依赖", { timeout: 20000 }, () => {
    assert.strictEqual(existsSync(path.join(SCRIPT_DIR, "..", "SKILL.md")), true);
    assert.strictEqual(existsSync(path.join(SCRIPT_DIR, "..", "skill.json")), true);
    const skill = JSON.parse(readFileSync(path.join(SCRIPT_DIR, "..", "skill.json"), "utf8"));
    assert.strictEqual(skill.id, "tool-split-chapters");
    assert.strictEqual(skill.permissions.shell, true);
    // 零第三方依赖：所有 import 都必须来自 node: 内置模块
    const source = readFileSync(SCRIPT_PATH, "utf8");
    const specifiers = Array.from(source.matchAll(/from\s+["']([^"']+)["']/g)).map((match) => match[1]);
    assert.ok(specifiers.length > 0);
    assert.strictEqual(specifiers.every((specifier) => specifier.startsWith("node:")), true);
  });
});

describe("tool-split-chapters · JSON 键名守卫", () => {
  test("全部产出 JSON 的键名均为 camelCase（^[a-z][A-Za-z0-9]*$，不含下划线），漏改即失败", { timeout: 30000 }, () => {
    const target = outDir("key-guard");
    // 一次运行覆盖全部产物形态：重复资产（duplicates / ignoredInputs）、GBK 回退（encodingFallbacks）、
    // 缺号 / 重复章名 / 乱序 / 正文过短 / 污染 / 未识别标题行 / 弱标题，以及 rename 修订（previousTitle）。
    const result = runCli([
      "--input",
      fixturePath("guardmain.txt"),
      "--input",
      fixturePath("guardnum.txt"),
      "--input",
      fixturePath("gbk.txt"),
      "--input",
      fixturePath("guarda.txt"),
      "--input",
      fixturePath("guardb.txt"),
      "--revisions",
      JSON.stringify({ ops: [{ op: "rename", asset: "guardnum", chapter: 1, title: "1、第一段（改）" }] }),
      "--out",
      target,
      "--json",
    ]);
    assert.strictEqual(result.stderr, "");
    assert.strictEqual(result.code, 0);

    // 第 1 项守卫：源包 JSON 文件清单固定为这 5 个（中文文件名保持不变）
    const jsonFiles = readdirSync(target, { withFileTypes: true })
      .filter((entry) => entry.isFile() && entry.name.endsWith(".json"))
      .map((entry) => entry.name)
      .sort();
    assert.deepStrictEqual(jsonFiles, ["manifest.json", "章节索引.json", "合并章节索引.json", "指纹.json", "批次计划.json"].sort());

    // 第 2 项守卫：递归收集全部产出的 JSON 键名（含嵌套对象与数组元素）
    const collected = [];
    for (const name of jsonFiles) {
      collectJsonKeys(readJson(path.join(target, name)), name, collected);
    }
    assert.ok(collected.length > 200);

    // 第 3 项守卫：逐个键名断言 camelCase，任何下划线残留都会在这里失败
    const offenders = collected.filter((item) => !/^[a-z][A-Za-z0-9]*$/.test(item.key));
    assert.deepStrictEqual(offenders.map((item) => `${item.where} <- ${item.key}`), []);
    const underscores = collected.filter((item) => item.key.includes("_"));
    assert.deepStrictEqual(underscores.map((item) => `${item.where} <- ${item.key}`), []);
  });
});

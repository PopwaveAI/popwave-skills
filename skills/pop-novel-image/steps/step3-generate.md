# Step 3: 执行生成

> 确定参数 → 执行API → 保存图片 → 回写记录

## 1. 确定参数

| 参数 | 默认值 | 说明 |
|:-----|:-------|:-----|
| model | `doubao-seedream-5-0-pro-260628` | Seedream 5.0 Pro |
| size | 按画幅选择 | 见速查表 |
| watermark | `false` | 不加水印 |
| response_format | `url` | 返回URL，脚本自动下载 |

### 尺寸速查

| 比例 | 像素 | 用途 |
|:-----|:-----|:-----|
| 3:4 | 1125x1500 | 竖版（默认） |
| 4:3 | 1500x1125 | 横版 |
| 1:1 | 1500x1500 | 方形 |
| 16:9 | 1500x844 | 宽屏 |
| 9:16 | 844x1500 | 竖版海报 |

## 2. 执行生成

```powershell
python scripts/generate.py image --prompt "提示词内容" --model doubao-seedream-5-0-pro-260628 --size 1125x1500 --output "素材/视觉/生成-v1.png"
```

图生图模式（有参考图时）：
```powershell
python scripts/generate.py image --prompt "提示词内容" --model doubao-seedream-5-0-pro-260628 --size 1125x1500 --image "data:image/png;base64,<base64数据>" --output "素材/视觉/生成-v1.png"
```

## 3. 输出目录

确保输出目录存在：`素材/视觉/`，如不存在则创建。

## 4. 回写提示词记录

在项目文件中追加：

```markdown
## 生成 1 | [日期]
- 模型：Seedream 5.0 Pro
- 画风：[画风名]
- 光照模板：[LT1/LT2/LT3]
- 构图模板：[CT1/CT2]
- 提示词：[完整提示词]
- 尺寸：[尺寸]
- 输出：[路径]
- 状态：✅ 生成成功
```

## 5. 迭代

如果用户对结果不满意：
1. 诊断问题：画风辨识度不足→强化dna描述；光照不兼容→换模板；人物变形→加约束
2. 调整提示词对应维度
3. 重新生成（文件名递增v2, v3...）
4. 更新记录

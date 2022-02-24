## 调用方法

+ `XXX_path` 的值可以省略后缀(默认会使用`.qasm`)
+ `PatternMatching` 返回的 `mappingList` 实际是 `(M, patternGraph)`。其中 M是`<Mstr, Msem>`的数组。所以如果要列出 Mstr 应当：
  ```python
   for m in mappingList[0]:
       print(m.Mstr)
   # mappingList[1] is patternGraph
  ```
+ `ReplaceSubgraph` 返回的 `rewrittenGraph` 上可以调用 `saveQASM` 将最终结果保存至 qasm 文件
 
 ```python
from PatternMatching import PatternMatching
from ReplaceSubgraph import ReplaceSubgraph

data_path = './data/origin/example.qasm'
pattern_path = './data/pattern/pattern.qasm'
substitute_path = './data/pattern/substitute.qasm'


# # Algorithm 1: return mapping list M
mappingList = PatternMatching(data_path, pattern_path)

# # Algorithm 2: return rewritten graph Gr
rewrittenGraph = ReplaceSubgraph(data_path, substitute_path, mappingList)
rewrittenGraph.saveQASM('result.qasm')
 ```
 
## 实例

### 1. pattern: CX CX => _

+ before pattern mapping:
  
  <img src="https://github.com/ShepherdLee519/CircuitRewriting/blob/main/image/example1-before.PNG" width=450 />
+ after pattern mapping:
  
  <img src="https://github.com/ShepherdLee519/CircuitRewriting/blob/main/image/example1-after.PNG" width=450 />
  
### 2. pattern: X X => _

+ before pattern mapping:
  
  <img src="https://github.com/ShepherdLee519/CircuitRewriting/blob/main/image/example2-before.PNG" width=450 />
+ after pattern mapping:
  
  <img src="https://github.com/ShepherdLee519/CircuitRewriting/blob/main/image/example2-after.PNG" width=450 />

### 3. pattern: X CX X => CX

<pre>
 ----- o -----                 --- o ---
       |              =            |
 - X - @ - X -                 --- @ --- 
</pre>

+ before pattern mapping:
  
  <img src="https://github.com/ShepherdLee519/CircuitRewriting/blob/main/image/example3-before.PNG" width=450 />
+ after pattern mapping:
  
  <img src="https://github.com/ShepherdLee519/CircuitRewriting/blob/main/image/example3-after.PNG" width=450 />
  
### 4. pattern: CX CX CX => CX CX

<pre>
 - o ----- o -                   - o -----
   |       |                       | 
 - @ - o - @ -        =          --|-- o - 
       |                           |   |
 ----- @ -----                   - @ - @ - 
</pre>

+ before pattern mapping:
  
  <img src="https://github.com/ShepherdLee519/CircuitRewriting/blob/main/image/example4-before.PNG" width=450 />
+ after pattern mapping:
  
  <img src="https://github.com/ShepherdLee519/CircuitRewriting/blob/main/image/example4-after.PNG" width=450 />

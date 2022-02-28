## 调用方法

```python
from CircuitWriter import CircuitWriter

data_path = './data/origin/' # folder path or file path
pattern_path = './data/pattern/' # folder path or file path
output_path = './data/result/' # should be a folder path


circuitWriter = CircuitWriter()
circuitWriter.execute(data_path, pattern_path, output_path)
```

### 输出：

```
Start Timer: [Solving <./data/origin/example1.qasm>]
 - finished. (before: 11, after: 5, reduced: 6(54.55%))
End Timer [Solving <./data/origin/example1.qasm>]:  0.9433407783508301

Start Timer: [Solving <./data/origin/example2.qasm>]
 - finished. (before: 11, after: 3, reduced: 8(72.73%))
End Timer [Solving <./data/origin/example2.qasm>]:  1.7841272354125977

Start Timer: [Solving <./data/origin/example3.qasm>]
 - finished. (before: 10, after: 4, reduced: 6(60.00%))
End Timer [Solving <./data/origin/example3.qasm>]:  1.618220329284668

Start Timer: [Solving <./data/origin/example4.qasm>]
 - finished. (before: 12, after: 8, reduced: 4(33.33%))
End Timer [Solving <./data/origin/example4.qasm>]:  2.696258783340454

Start Timer: [Solving <./data/origin/example5.qasm>]
 - finished. (before: 18, after: 8, reduced: 10(55.56%))
End Timer [Solving <./data/origin/example5.qasm>]:  2.8672003746032715
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

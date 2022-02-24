## 调用方法

 ```python
from CircuitWriter import CircuitWriter

data_path = './data/origin/example.qasm'
pattern_path = './data/pattern/pattern.json'


circuitWriter = CircuitWriter()
result = circuitWriter.execute(data_path, pattern_path)
result.saveQASM('result.qasm')
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

# 3dshadowpy

### 22-03-2022
- fix saturation to 100
- only exposure value is adjust based on color saturation of object 
- use mean of saturation from HSV color model to extract object
- segmented object is used to extract shadow with basic bitwise operator (XOR)
- object skeleton is used to compute height from cated shadow length 

### To do
- [ ] add quoue.get() before every quoue.put() to free before new push data to preventing memory leaks. 
- [ ] clean code
- [ ] change gui by remove HSV slider of shadow on object
- [ ] fix bug when process image has problem to continuous process or indicating to user  

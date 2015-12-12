# Filters

Utiliza Python 2.7. La referenca para PySide está [aquí](http://pyside.github.io/). Y ejemplos [acá](https://github.com/PySide/Examples/tree/050809faad4e8f58e89ab53df9e3f86045f98c48/examples/widgets).

## Librerías
 - PySide
 - matplotlib

## Fuentes
 - [Lowpass](http://sim.okawa-denshi.jp/en/CRhikeisan.htm)
 - [Highpass](http://sim.okawa-denshi.jp/en/LRlowkeisan.htm)
 - [Bandpass](http://sim.okawa-denshi.jp/en/RLCbpkeisan.htm)
 - [Bandstop](http://sim.okawa-denshi.jp/en/RLCbekeisan.htm)

## ITL
Description of a Linear time-invariant system, described by it's zeros, poles and gain. Gain is zero for all filters `20*log(1) = 0`. A resistance of 1 Ohm is considered for all filters.

```
scipy.signal.lti(zeros, poles, gain)
```

### RL
`(R/L)/(S+(R/L))`

zeros = `[]`
poles = `[-1/L]`
gain = `0`

### CR
`S/(S+(1/CR))`

zeros = `[0]`
poles = `[-1/C]`
gain = `0`

### LCR (Bandpass)
`((R/L)S)/(S**2+S(R/L)+(1/LC))`

zeros = `[0, float("inf")]`
poles = `[((-1/L)-(1/L)*(C-4L))/2,((-1/L)+(1/L)*(C-4L))/2]`
gain = `0`

### RLC (Bandstop)
`((s**2)+(1/LC))/(S**2+S(R/L)+(1/LC))`

zeros = `[(-1/LC)**(1/2),-(-1/LC)**(1/2)]`
poles = `[((-1/L)-(1/L)*(C-4L))/2,((-1/L)+(1/L)*(C-4L))/2]`
gain = `0`

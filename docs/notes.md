## obstacle (bounce) implementation

* obstacle is encoded on 8th bit (0b1000_000)
* when particles meets obstacle their bits rotate 
  - HPP 2 times (to the left or to the right) eg 0x1100 -> 0x10000000 -> 0x10000011
  - FHP* 3 times (to the left or to the right)
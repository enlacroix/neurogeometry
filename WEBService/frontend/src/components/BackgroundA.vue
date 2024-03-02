<template>
  <ul class="background">
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
  </ul>
</template>

<script>
export default {
  name: "MainBackground"
}
</script>

<style lang="sass">
@keyframes animate
  0%
    transform: translateY(0) rotate(0deg)
    opacity: 1
    border-radius: 0
  100%
    transform: translateY(-1000px) rotate(720deg)
    opacity: 0
    border-radius: 50%



.background
  position: fixed
  width: 100vw
  height: calc(100vh - 60px)
  top: 60px
  left: 0
  margin: 0
  padding: 0
  background: white
  overflow: hidden

.background li
  position: absolute
  display: block
  list-style: none
  width: 20px
  height: 20px
  background: rgba(172, 212, 255, 0.25)
  animation: animate 31s linear infinite





.background li:nth-child(0)
  left: 3%
  width: 59px
  height: 59px
  bottom: -59px
  animation-delay: 1s

.background li:nth-child(1)
  left: 63%
  width: 124px
  height: 124px
  bottom: -124px
  animation-delay: 3s

.background li:nth-child(2)
  left: 35%
  width: 197px
  height: 197px
  bottom: -197px
  animation-delay: 2s

.background li:nth-child(3)
  left: 84%
  width: 54px
  height: 54px
  bottom: -54px
  animation-delay: 14s

.background li:nth-child(4)
  left: 14%
  width: 156px
  height: 156px
  bottom: -156px
  animation-delay: 7s

.background li:nth-child(5)
  left: 89%
  width: 164px
  height: 164px
  bottom: -164px
  animation-delay: 7s

.background li:nth-child(6)
  left: 69%
  width: 189px
  height: 189px
  bottom: -189px
  animation-delay: 22s

.background li:nth-child(7)
  left: 8%
  width: 59px
  height: 59px
  bottom: -59px
  animation-delay: 2s

.background li:nth-child(8)
  left: 5%
  width: 116px
  height: 116px
  bottom: -116px
  animation-delay: 21s

.background li:nth-child(9)
  left: 62%
  width: 130px
  height: 130px
  bottom: -130px
  animation-delay: 11s

.background li:nth-child(10)
  left: 12%
  width: 71px
  height: 71px
  bottom: -71px
  animation-delay: 45s

.background li:nth-child(11)
  left: 53%
  width: 89px
  height: 89px
  bottom: -89px
  animation-delay: 14s

.background li:nth-child(12)
  left: 32%
  width: 137px
  height: 137px
  bottom: -137px
  animation-delay: 53s

.background li:nth-child(13)
  left: 10%
  width: 141px
  height: 141px
  bottom: -141px
  animation-delay: 10s

.background li:nth-child(14)
  left: 89%
  width: 95px
  height: 95px
  bottom: -95px
  animation-delay: 50s

.background li:nth-child(15)
  left: 12%
  width: 139px
  height: 139px
  bottom: -139px
  animation-delay: 26s

@media (max-width: 1100px)
  @keyframes animate
    0%
      transform: translateY(0) rotate(0deg)
      opacity: 1
      border-radius: 0
    100%
      transform: translateY(-1000px) rotate(720deg)
      opacity: 0
      border-radius: 50%



  .background
    position: fixed
    width: 100vw
    height: calc(100vh - 60px)
    top: 60px
    left: 0
    margin: 0
    padding: 0
    background: white
    overflow: hidden

  .background li
    position: absolute
    display: block
    list-style: none
    width: 20px
    height: 20px
    background:  rgba(172, 212, 255, 0.25)
    animation: animate 31s linear infinite



  .background li:nth-child(0)
    left: 39%
    width: 58px
    height: 58px
    bottom: -58px
    animation-delay: 25s

  .background li:nth-child(1)
    left: 70%
    width: 51px
    height: 51px
    bottom: -51px
    animation-delay: 4s

  .background li:nth-child(2)
    left: 39%
    width: 110px
    height: 110px
    bottom: -110px
    animation-delay: 13s

  .background li:nth-child(3)
    left: 27%
    width: 108px
    height: 108px
    bottom: -108px
    animation-delay: 3s

  .background li:nth-child(4)
    left: 4%
    width: 118px
    height: 118px
    bottom: -118px
    animation-delay: 10s

  .background li:nth-child(5)
    left: 13%
    width: 103px
    height: 103px
    bottom: -103px
    animation-delay: 19s

  .background li:nth-child(6)
    left: 45%
    width: 56px
    height: 56px
    bottom: -56px
    animation-delay: 28s

  .background li:nth-child(7)
    left: 4%
    width: 91px
    height: 91px
    bottom: -91px
    animation-delay: 4s

  .background li:nth-child(8)
    left: 35%
    width: 71px
    height: 71px
    bottom: -71px
    animation-delay: 36s

  .background li:nth-child(9)
    left: 80%
    width: 97px
    height: 97px
    bottom: -97px
    animation-delay: 43s

  .background li:nth-child(10)
    left: 67%
    width: 122px
    height: 122px
    bottom: -122px
    animation-delay: 27s

  .background li:nth-child(11)
    display: none

  .background li:nth-child(12)
    display: none

  .background li:nth-child(13)
    display: none

  .background li:nth-child(14)
    display: none

  .background li:nth-child(15)
    display: none


</style>
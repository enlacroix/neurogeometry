<template>
  <button class="button">
    <slot>

    </slot>
  </button>
</template>

<script>
export default {
  name: "button-a"
}
</script>

<style lang="sass">

.button
    background: rgb(204, 228, 255)
    border-radius: 20px 0px 20px 0px
    padding: 12px 30px
    color: black
    border: 2.4px solid #264C96FF
    &:hover
        background: $light-blue
    &:focus
        outline: none

@media (min-width: 768px)
    .button
        padding: 16px 44px


</style>
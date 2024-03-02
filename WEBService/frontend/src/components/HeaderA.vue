<template>
  <header class="header" >
    <div class="container">
      <nav>
        <div class="navbar">
          <div class="navbar__name">
            <a class="navbar__logo" href="#">
              <img src="@/assets/logo.png" id="navbar_logo">
              <div class="navbar__logo-text"><span>Нейрогеометрия</span></div>
            </a>
          </div>
          <button
              @click="toggleMobile"
              class="navbar__toggle" :class="{'navbar__toggle_active': view.isMobileOpen}">
            <div class="navbar__togline navbar__togline_1"></div>
            <div class="navbar__togline navbar__togline_2"></div>
            <div class="navbar__togline navbar__togline_3"></div>
          </button>
          <ul v-show="!view.isMobile" class="nav">
            <li class="nav__item">
              <a @click="showSettings" href="#">Настройки</a>
            </li>
             <li class="nav__item">
              <a @click="showExamples" href="#">Примеры</a>
            </li>
            <li class="nav__item">
              <a @click="showHelp" href="#">Справка</a>
            </li>
          </ul>
          <ul v-show="view.isMobile" class="nav"
              :class="{'nav__active': view.isMobileOpen}">
            <li class="nav__item">
              <a @click="showSettings" href="#">Настройки</a>
            </li>
             <li class="nav__item">
              <a @click="showExamples" href="#">Примеры</a>
            </li>
            <li class="nav__item">
              <a @click="showHelp" href="#">Справка</a>
            </li>
          </ul>
        </div>
      </nav>
    </div>
  </header>
  <dialog-a v-model:show="view.ExampleVisible">
    <examples-a
        @switchToHelp="compute_switch"
    />
  </dialog-a>
  <dialog-a v-model:show="view.HelpVisible">
    <help-text-a
        @give_command="get_command"
    />
  </dialog-a>
  <dialog-a v-model:show="view.SettingsVisible">
    <settings-a
        :settings_prop="settings_prop"
        @give_settings="get_settings"
    />
  </dialog-a>
</template>

<script>
import HelpTextA from "@/components/HelpTextA";
import SettingsA from "@/components/SettingsA";
import ExamplesA from "@/components/ExamplesA";

export default {
  name: "header-a",
  components: {ExamplesA, HelpTextA, SettingsA},
  props: {
    settings_prop: {
      type: Object,
      default: {
        is_full_searching: false,
        variables_limit: 50,
        max_iter_amount: 10,
        use_linear_angle_method: false,
      },
      required: true,
    },
  },
  data() {
    return {
      view: {
        topOfPage: true,
        isMobileOpen: false,
        isMobile: false,
        windowWidth: null,

        ExampleVisible: false,
        HelpVisible: false,
        SettingsVisible: false,
      },
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
  },
  methods: {
    hideMobileNav() {
      this.view.isMobileOpen = false;
    },
    checkScreen() {
      this.view.windowWidth = window.innerWidth;
      this.view.isMobile = this.view.windowWidth <= 768;
      if (!this.view.isMobile) this.hideMobileNav();
    },
    toggleMobile() {
      if (this.view.isMobile) {
        this.view.isMobileOpen = !this.view.isMobileOpen;
      }
    },
    showHelp() {
      this.view.HelpVisible = true;
      this.hideMobileNav();
    },
    showSettings() {
      this.view.SettingsVisible = true;
      this.hideMobileNav();
    },
    showExamples() {
      this.view.ExampleVisible = true;
      this.hideMobileNav();
    },
    get_command(command_) {
      this.view.HelpVisible = false;
      this.$emit('give_command', command_);
    },
    get_settings(settings_) {
      this.view.SettingsVisible = false;
      this.$emit('give_settings', settings_);
    },
    compute_switch(param_) {
      this.view.ExampleVisible = param_;
      if (!this.view.ExampleVisible) this.showHelp();
    }
  }
}
</script>

<style lang="sass">
.header
    position: fixed
    z-index: 2000
    width: 100%
    border-bottom: none
    transition: background-color .2s, border-color .2s
    background-color: $light-blue
    border-bottom: $main-border

#navbar_logo
    position: relative
    top: -5px
    width: 35px
    margin-right: 5px


.navbar
    display: flex
    flex-wrap: wrap
    align-items: center
    justify-content: space-between
    a
        text-decoration: none
        color: black
    &__name
        a:hover
            text-decoration: none
            color: black
    &__toggle
        display: none
    &__logo
        display: flex
        align-items: center
        height: $header-height
        &-text
            padding-left: 1rem

.nav
    list-style-type: none
    padding: 0
    margin: 0
    display: flex
    &__item
        padding: 0 2rem
        &:last-child
            padding-right: 0
        a
            padding: 0.5rem

@media (max-width: 768px)
    .navbar
        &__toggle
            display: block
            border: none
            padding: 1rem 0
            background-color: rgba(0, 0, 0, 0)
            outline: 0 !important
            &_active
                .navbar__togline
                    &_1
                        transform: translateY(1.5px) rotate(45deg)
                    &_2
                        background-color: rgba(0, 0, 0, 0)
                    &_3
                        transform: translateY(-1.5px) rotate(-45deg)
        &__togline
            height: 1.5px
            width: 20px
            background-color: black
            &_1
                transform: translateY(-5px)
            &_3
                transform: translateY(5px)

    .nav
        width: 100%
        padding: 0
        flex-wrap: wrap
        overflow: hidden
        height: 0
        &__active
          height: 30%
        &__item
            padding: 0
            width: 100%
            &:last-child
                margin-bottom: 0.5rem
            &:first-child
                margin-top: 0.5rem
            a
                display: block
                padding: 0.5rem 0

</style>
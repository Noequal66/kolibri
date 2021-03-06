<template>

  <core-modal
    :title="$tr('title')"
    :invisibleTitle="true"
    :enableBgClickCancel="true"
    :hasError="wrongCreds"
    @enter="userLogin"
    @cancel="cancelLoginModal"
  >
    <div class="title">
      <div class="login-brand-box">
        <img src="./icons/kolibri-logo.svg" alt="">
        <p id="login-brand">{{ $tr('kolibri') }}</p>
      </div>
    </div>
    <div>
      <div v-if="wrongCreds" class="error-wrapper">
        <h1>{{ $tr('logInError') }}</h1>
        <span aria-live="polite">{{ $tr('validationError') }}<br>{{ $tr('tryAgain') }}</span>
      </div>
      <div>
        <mat-svg category="social" name="person"/>
        <input
          type="text"
          class="login-form login-username"
          autofocus
          v-model="username_entered"
          ref="usernamefield"
          :placeholder="$tr('userName')"
          :aria-label="$tr('userName')"
        >
      </div>
      <div>
        <mat-svg category="action" name="lock"/>
        <input
          type="password"
          class="login-form login-password"
          v-model="password_entered"
          :placeholder="$tr('password')"
          :aria-label="$tr('password')"
        >
      </div>
      <button class="login-button" @click="userLogin">{{ $tr('logIn') }}</button>
    </div>
  </core-modal>

</template>


<script>

  const actions = require('kolibri.coreVue.vuex.actions');

  module.exports = {
    $trNameSpace: 'loginModal',
    $trs: {
      title: 'Log in to Kolibri',
      logIn: 'Log In',
      kolibri: 'Kolibri',
      logInError: 'Log-in Error',
      validationError: 'Incorrect username or password.',
      tryAgain: 'Please try again!',
      userName: 'Username',
      password: 'Password',
    },
    components: {
      'core-modal': require('kolibri.coreVue.components.coreModal'),
    },
    data: () => ({
      username_entered: '',
      password_entered: '',
    }),
    mounted() {
      this.$nextTick(() => {
        this.$refs.usernamefield.focus();
      });
      this.username_entered = '';
      this.password_entered = '';
    },
    methods: {
      userLogin() {
        const payload = {
          username: this.username_entered,
          password: this.password_entered,
        };
        this.kolibriLogin(payload);
        this.$refs.usernamefield.focus();
      },
    },
    vuex: {
      getters: {
        wrongCreds: state => state.core.loginError === 401,
      },
      actions: {
        cancelLoginModal: actions.cancelLoginModal,
        kolibriLogin: actions.kolibriLogin,
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'
  @require '~kolibri.styles.navBarItem'

  h1
    font-size: 1.1em

  .login-button
    width: 300px
    display: block
    margin: 20px auto
    padding: 8px
    background: $core-action-normal
    color: white
    font-size: 16px
    transition: 0.15s
    &:hover
      background: $core-action-dark
      padding: 8px

  .login-brand-box
    text-align: center
    margin: 15px 5px auto
    img, p
      display: inline-block
    img
      max-width: 100px
      height: auto
      position: relative
      top: 20px
      right: 10px

  #login-brand
    font-size: 50px
    letter-spacing: 0.1em
    font-weight: 100
    color: $core-action-normal
    margin-bottom: 15px

  .login-form
    width: 275px
    margin: 0 auto
    display: inline-block
    padding-top: 5px
    padding-bottom: 5px
    letter-spacing: 0.08em
    border: none
    border-bottom: 1px solid $core-text-default
    height: 30px
    &:focus
      outline: none
      border-bottom: 3px solid $core-action-normal

  .login-username
    margin: 30px auto
    transition: all 0.15s

  .login-password
    transition: all 0.15s

  .error-wrapper
    text-align: center

  svg
    vertical-align: middle

</style>

<template>

  <div class="nav-wrapper">
    <nav class="nav-main" role="navigation" :aria-label="ariaLabel">
      <nav-bar-item href="/learn/#/learn" :active="learnActive">
        <mat-svg class="nav-icon" category="action" name="home"/>
        <div class="label">{{ $tr('learn') }}</div>
      </nav-bar-item>
      <nav-bar-item href="/learn/#/explore" :active="exploreActive">
        <mat-svg class="nav-icon" category="action" name="explore"/>
        <div class="label">{{ $tr('explore') }}</div>
      </nav-bar-item>
      <nav-bar-item v-if="isCoachAdminOrSuperuser" href="/coach" :active="coachActive">
        <mat-svg class="nav-icon" category="action" name="assessment"/>
        <div class="label">{{ $tr('coach') }}</div>
      </nav-bar-item>
      <nav-bar-item v-if="loggedIn" href="/management" :active="profileActive">
        <mat-svg class="nav-icon" category="social" name="people"/>
        <div class="label">{{ $tr('profile') }}</div>
      </nav-bar-item>
      <nav-bar-item v-if="loggedIn">
        <mat-svg class="nav-icon" category="social" name="people"/>
        <div class="label">{{ $tr('logOut') }}</div>
      </nav-bar-item>
      <nav-bar-item v-else href="/signin">
        <mat-svg class="nav-icon" category="social" name="people"/>
        <div class="label">{{ $tr('signIn') }}</div>
      </nav-bar-item>
      <session-nav-widget/>
      <div>
        Kolibri Version: {{ version }}
      </div>
    </nav>

    <!-- log-in modal -->
    <login-modal v-if="loginModalVisible"/>
  </div>

</template>


<script>

  const values = require('lodash.values');
  const getters = require('kolibri.coreVue.vuex.getters');
  const TopLevelPageNames = require('kolibri.coreVue.vuex.constants').TopLevelPageNames;
  const UserKinds = require('kolibri.coreVue.vuex.constants').UserKinds;


  module.exports = {
    $trNameSpace: 'navbar',
    $trs: {
      navigationLabel: 'Main user navigation',
      learn: 'Learn',
      explore: 'Explore',
      manage: 'Manage',
      coach: 'Coach',
      signIn: 'Sign in',
      profile: 'Profile',
      logOut: 'Log out',
    },
    props: {
      topLevelPageName: {
        type: String,
        validator(value) {
          if (!value) {
            return true; // Okay if it's undefined
          }
          return values(TopLevelPageNames).includes(value);
        },
      },
    },
    data: () => ({
      version: __version, // eslint-disable-line no-undef
    }),
    computed: {
      ariaLabel() {
        return this.$tr('navigationLabel');
      },
      learnActive() {
        return this.topLevelPageName === TopLevelPageNames.LEARN_LEARN;
      },
      exploreActive() {
        return this.topLevelPageName === TopLevelPageNames.LEARN_EXPLORE;
      },
      coachActive() {
        return this.topLevelPageName === TopLevelPageNames.COACH;
      },
      manageActive() {
        return this.topLevelPageName === TopLevelPageNames.MANAGE;
      },
      profileActive() {
        return this.topLevelPageName === TopLevelPageNames.PROFILE;
      },
    },
    components: {
      'session-nav-widget': require('kolibri.coreVue.components.sessionNavWidget'),
      'nav-bar-item': require('kolibri.coreVue.components.navBarItem'),
      'login-modal': require('kolibri.coreVue.components.loginModal'),
    },
    vuex: {
      getters: {
        session: state => state.core.session,
        loggedIn: state => state.core.session.kind[0] !== UserKinds.ANONYMOUS,
        isAdminOrSuperuser: getters.isAdminOrSuperuser,
        isCoachAdminOrSuperuser: getters.isCoachAdminOrSuperuser,
        loginModalVisible: state => state.core.loginModalVisible,
      },
    },
  };

</script>


<style lang="stylus" scoped>

  @require '~kolibri.styles.definitions'
  @require '~kolibri.styles.navBarItem'

  .nav-wrapper
    display: table
    table-layout: fixed
    background: $core-bg-light
    font-weight: 300
    position: fixed
    z-index: auto
    @media screen and (min-width: $portrait-breakpoint + 1)
      font-size: 1em
      height: 100%
      width: $nav-width
    @media screen and (max-width: $portrait-breakpoint)
      font-size: 0.8em
      bottom: 0
      width: 100%
      min-width: 300px

  .nav-main
    background: $core-bg-light
    height: 100vh
    @media screen and (max-width: $portrait-breakpoint)
      display: table-row
      height: 56px

  a.active:focus svg
    fill: $core-bg-light

  .nav-icon
    width: 40px
    height: 40px

</style>

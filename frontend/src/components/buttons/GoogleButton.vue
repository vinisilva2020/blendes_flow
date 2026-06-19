<script setup lang="ts">
import googleLogo from '@/assets/img/google.svg'
</script>
<template>
    <button
        class="inline-flex min-h-11 w-full cursor-pointer items-center justify-center gap-2.5 rounded-lg border border-[#d8e6e9] bg-white px-4 text-sm font-extrabold leading-none text-[#172224] shadow-[0_12px_26px_rgb(18_33_36_/_7%),inset_0_1px_0_rgb(255_255_255_/_90%)] transition duration-180 hover:-translate-y-px hover:border-[#b5d2d8] hover:shadow-[0_16px_34px_rgb(18_33_36_/_11%),0_0_20px_rgb(174_238_255_/_14%),inset_0_1px_0_#fff] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/60 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
        type="button"
      >
        <img class="block size-5" :src="googleLogo" alt="" aria-hidden="true" />
        <span>Entrar com Google</span>
      </button>
</template>
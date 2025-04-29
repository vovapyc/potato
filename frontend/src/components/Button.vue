<script setup lang="ts">
const { disabled } = defineProps<{
    disabled?: boolean;
}>();
</script>

<template>
    <button :class="[
        'px-6 py-2 text-sm font-mono border-4 transition uppercase bg-gray-200 text-black border-gray-700',
        disabled
            ? 'cursor-not-allowed line-through'
            : 'hover:bg-gray-300 active:bg-gray-400 cursor-pointer'
    ]" :disabled="disabled">
        <slot />
    </button>
</template>

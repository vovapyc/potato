<script setup lang="ts">
// This component must be inside block with relative position
// it's not the best solution, but it works 😬

const { status } = defineProps<{
    status: "processing" | "yes" | "no" | "error" | null;
}>();
</script>

<template>
    <div v-if="status !== null" :class="[
        'absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 px-6 py-1 rounded-full text-center press-start-2p-regular text-lg uppercase shadow-md text-black',
        status === 'processing' ? 'bg-yellow-300' :
            status === 'yes' ? 'bg-green-300' :
                status === 'no' ? 'bg-red-400' : 'bg-red-500'
    ]">
        {{ status }}
    </div>
</template>
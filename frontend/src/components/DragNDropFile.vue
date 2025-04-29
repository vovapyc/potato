<script setup lang="ts">
import { ref } from 'vue';

const { uploadFunc, fileChangeFunc } = defineProps<{
    uploadFunc: (event: Event) => void;
    fileChangeFunc: (event: Event) => void;
}>();

const isDragging = ref<boolean>(false);
const onDrop = (event: DragEvent) => {
    const file = event.dataTransfer?.files[0];
    if (file) {
        const fakeEvent = { target: { files: [file] } } as unknown as Event;
        fileChangeFunc(fakeEvent);
    }
};
const onDropAndReset = (event: DragEvent) => {
    isDragging.value = false;
    onDrop(event);
};
</script>

<template>
    <div class="w-full max-w-md h-64 flex items-center justify-center text-center cursor-pointer border-4 border-dashed"
        :class="[
            isDragging ? 'border-yellow-400 bg-yellow-100' : 'border-gray-400 bg-transparent'
        ]" @click="uploadFunc" @dragenter.prevent="isDragging = true" @dragleave.prevent="isDragging = false"
        @dragover.prevent @drop.prevent="onDropAndReset">
        <p v-html="isDragging ? 'Drop your potato here' : 'Drag and drop your potato picture<br>or click to upload'"
            class="text-gray-400 font-mono pointer-events-none"></p>
    </div>
</template>
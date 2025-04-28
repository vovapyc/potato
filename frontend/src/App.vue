<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Button from './components/Button.vue';

const imageSrc = ref<string | null>(null);
const isProcessing = ref<boolean>(false);
const isCameraAvailable = ref<boolean>(true);

const triggerUpload = () => {
  // Click the hidden file input to open the file picker
  // Hidden input needed to style the file input
  // and to prevent the default file input behavior
  const fileInput = document.getElementById('fileInput') as HTMLInputElement;
  fileInput?.click();
};

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    imageSrc.value = URL.createObjectURL(file);
    isProcessing.value = true;
  }
};

const startCamera = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: 'environment' } }
    });
    const video = document.getElementById('video') as HTMLVideoElement;
    if (video) {
      video.srcObject = stream;
      isCameraAvailable.value = true;
    }
  } catch (err) {
    console.error('Error accessing camera', err);
    isCameraAvailable.value = false;
  }
};

const capturePhoto = () => {
  const video = document.getElementById('video') as HTMLVideoElement;
  if (!video) return;
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const context = canvas.getContext('2d');
  if (context) {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    imageSrc.value = canvas.toDataURL('image/png');
    isProcessing.value = true;
  }
};

const resetProcessing = () => {
  isProcessing.value = false;
  imageSrc.value = null;
  startCamera();
};

onMounted(() => {
  startCamera();
});
</script>

<template>
  <div
    class="block sm:hidden fixed inset-0 w-screen h-[100dvh] overflow-hidden flex flex-col items-center justify-between bg-black text-white p-4">
    <div class="flex flex-col items-center space-y-2">
      <h1 class="text-xl m-2 press-start-2p-regular uppercase">Is this a potato?</h1>
      <p class="text-xs text-gray-400 font-mono">Certified Potato Classifier 🥔</p>
    </div>

    <div class="flex-1 flex items-center justify-center w-full overflow-hidden">
      <div class="bg-gray-800 w-full max-w-sm aspect-square flex items-center justify-center">
        <input type="file" accept="image/*" class="hidden" id="fileInput" @change="onFileChange" />
        <img v-if="imageSrc" :src="imageSrc" alt="Uploaded" class="object-cover w-full h-full" />
        <template v-else>
          <div v-if="!isCameraAvailable" class="flex items-center justify-center text-center p-4 text-red-400 press-start-2p-regular text-xs uppercase leading-relaxed">
            Camera access denied<br />
            Please upload a photo
          </div>
          <video v-else id="video" autoplay muted playsinline class="object-cover w-full h-full"></video>
        </template>
      </div>
    </div>

    <div class="flex justify-around w-full max-w-sm mb-6">
      <template v-if="!isProcessing">
        <Button @click="triggerUpload">📂 Upload</Button>
        <Button @click="capturePhoto" :disabled="!isCameraAvailable">📷 Camera</Button>
      </template>
      <template v-else>
        <div class="flex justify-center w-full">
          <Button @click="resetProcessing">🔄 Classify more</Button>
        </div>
      </template>
    </div>
  </div>

  <div class="hidden sm:block">Please use mobile version</div>
</template>

<style scoped>
html,
body,
#app {
  height: 100%;
  margin: 0;
}
</style>

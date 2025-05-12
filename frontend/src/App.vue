<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Button from './components/Button.vue';
import DragNDropFile from './components/DragNDropFile.vue';
import PotatoStatusLabel from './components/PotatoStatusLabel.vue';

const API_URL = "https://potato-api.fly.dev/predict/";

// It's needed to enable camera access on mobile devices
const MOBILE_BREAKPOINT_PX = 640;
const isMobile = ref<boolean>(window.innerWidth < MOBILE_BREAKPOINT_PX);

const imageSrc = ref<string | null>(null);
const isCameraAvailable = ref<boolean>(true);
const potatoStatus = ref<"processing" | "yes" | "no" | "error" | null>(null);

async function classifyImage(file: File | Blob) {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const resp = await fetch(API_URL, {
      method: 'POST',
      body: formData,
    });
    const data = await resp.json();
    potatoStatus.value = data.is_potato ? 'yes' : 'no';
  } catch (err) {
    console.error('API error', err);
    potatoStatus.value = 'error';
  }
}


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
    potatoStatus.value = "processing";
    classifyImage(file);
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
  if (!context) return;

  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Convert canvas to Blob and then handle upload
  canvas.toBlob((blob) => {
    if (blob) {
      // Preview via blob URL
      imageSrc.value = URL.createObjectURL(blob);
      potatoStatus.value = 'processing';
      classifyImage(blob);
    } else {
      console.error('Failed to capture image blob');
      potatoStatus.value = 'error';
    }
  }, 'image/jpeg');
};

const resetProcessing = () => {
  potatoStatus.value = null;
  imageSrc.value = null;
  if (isMobile.value) startCamera();
};

const updateIsMobile = () => {
  const wasMobile = isMobile.value;
  isMobile.value = window.innerWidth < 640;
  if (!wasMobile && isMobile.value) {
    startCamera();
  }
};

onMounted(() => {
  window.addEventListener('resize', updateIsMobile);
  if (isMobile.value) startCamera();
});
</script>

<template>
  <div :class="[
    'bg-black text-white p-4 items-center flex flex-col',
    isMobile ? 'fixed inset-0 w-screen h-[100dvh] justify-between' : 'justify-center min-h-screen space-y-6'
  ]">
    <div class="flex flex-col items-center space-y-2">
      <h1 class="text-xl m-2 press-start-2p-regular uppercase">Is this a potato?</h1>
      <p class="text-xs text-gray-400 font-mono">No potatoes were harmed during testing</p>
    </div>

    <input type="file" accept="image/*" class="hidden" id="fileInput" @change="onFileChange" />

    <div v-if="isMobile" class="flex-1 flex items-center justify-center w-full">
      <div class="bg-gray-800 w-full max-w-sm aspect-square flex flex-col relative">
        <potatoStatusLabel :status="potatoStatus" />
        <img v-if="imageSrc" :src="imageSrc" alt="Uploaded" class="object-cover w-full h-full" />
        <template v-else>
          <div v-if="!isCameraAvailable"
            class="flex items-center justify-center text-center text-red-400 press-start-2p-regular text-xs uppercase leading-relaxed">
            Camera access denied<br />
            Please upload a photo
          </div>
          <video v-else id="video" autoplay muted playsinline class="object-cover w-full h-full"></video>
        </template>
      </div>
    </div>

    <div v-if="!isMobile" class="items-center flex flex-col w-full">
      <div v-if="imageSrc" class="relative mt-6">
        <potatoStatusLabel :status="potatoStatus" />
        <img :src="imageSrc" alt="Uploaded" class="object-cover w-full h-full max-w-md aspect-square" />
      </div>
      <DragNDropFile v-else :uploadFunc="triggerUpload" :fileChangeFunc="onFileChange" />
    </div>

    <div class="flex justify-around w-full max-w-sm mb-6">
      <template v-if="isMobile && potatoStatus === null">
        <Button @click="triggerUpload">📂 Upload</Button>
        <Button @click="capturePhoto" :disabled="!isCameraAvailable">📷 Camera</Button>
      </template>
      <template v-if="potatoStatus !== null">
        <div class="flex justify-center w-full">
          <Button @click="resetProcessing">🔄 Classify more</Button>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
html,
body,
#app {
  height: 100%;
  margin: 0;
}
</style>

<template>
  <div>
    <p>Own Subject: {{ ownSubject }}</p>
    <p>Own Project: {{ ownProject }}</p>

    <h1 class="text-xxl">
      Subject detail for admin only create update
    </h1>
  </div>
</template>
/subject/detail-[subj_id]/index
  
<script lang="ts" setup>
// import { navigateTo } from '#app'
const router = useRouter()

const auth = useAuthStore()

const user = computed(() => auth.user)
const accessToken = computed(() => auth.accessToken)
const ownProject = computed(() => auth.ownProject)
const ownSubject = computed(() => auth.ownSubject)

onMounted(async () => {
  if (!auth.user || !auth.accessToken || !auth.refreshToken) {
    auth.loadFromCookies()
  }
})

const navigateTo = (path: string) => {
  router.push(path)
}
</script>
  
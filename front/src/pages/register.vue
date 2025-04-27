<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
        <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-md">
            <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">
                Create Account
            </h2>

            <form class="space-y-4" @submit="handleRegister">
                <!-- First Name -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                    <input v-model="inputVar.first_name" type="text" placeholder="John"
                        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <!-- Last Name -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                    <input v-model="inputVar.last_name" type="text" placeholder="Doe"
                        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <!-- Username -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
                    <input v-model="inputVar.username" type="text" placeholder="johndoe123"
                        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <!-- Email -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                    <input v-model="inputVar.email" ype="email" placeholder="you@example.com"
                        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <!-- Password -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                    <input v-model="inputVar.password" type="password" placeholder="••••••••"
                        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <!-- Confirm Password -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
                    <input v-model="inputVar.password2" type="password" placeholder="••••••••"
                        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <!-- Role -->

                <select v-model="inputVar.role" class="border px-3 py-2 rounded w-full">
                    <option value="" disabled selected>Select Role</option>
                    <option v-for="role in roles" :key="role.id" :value="role.name">{{ role.name }}</option>
                </select>


                <!-- Register Button -->
                <button type="submit"
                    class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition duration-200">
                    Register
                </button>
            </form>

            <!-- Login Link -->
            <p class="mt-4 text-center text-sm text-gray-600">
                Already have an account?
                <NuxtLink to="/login" class="text-blue-600 hover:underline">Log in</NuxtLink>
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">

definePageMeta({
    layout: 'homepage',
});
const auth = useAuthStore()
const inputVar = ref({
    username: '',
    password: "",
    password2: "",
    email: "",
    first_name: "",
    last_name: "",
    role: "",

})
type roleType = { id: number, name: string }
const roles = ref<roleType[]>([])

const handleRegister = async (e: Event) => {
    // prevent refresh page
    e.preventDefault()

    const payload = {
        username: inputVar.value.username,
        password: inputVar.value.password,
        password2: inputVar.value.password2,
        email: inputVar.value.email,
        first_name: inputVar.value.first_name,
        last_name: inputVar.value.last_name,
        role: inputVar.value.role ?? 'Student'
    }

    console.log('payload', payload)

    const res = await useFetch(
        'http://localhost:8000/auth/register/',
        {
            method: 'POST',
            // headers: {
            //     Authorization: `Bearer ${auth.accessToken}`,
            // },
            body: payload
        }
    )
    console.log('res', res)


    // return navigateTo('/login')
}


const getRoleList = async () => {
    try {
        const res = await useFetch(
            'http://localhost:8000/auth/roles',
            {
                method: 'GET',
            }
        )
        roles.value = res.data.value as roleType[];
    } catch (error) {
        console.error('Request failed:', error);
    }
}
const getAuth = async () => {
    auth.loadFromCookies()
}
onMounted(async () => {
    await getAuth();
    await getRoleList();
})
</script>
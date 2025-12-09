<template>
    <el-row style="margin-top: 3%;">
        <el-col :span="6" :offset="9">
            <el-card shadow="hover">
                <template #header>
                    <div class="login-header">
                        <span>Domo</span>
                    </div>
                </template>
                <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" style="padding: 5% 15% 0 15%;"
                    label-width="auto" size="default">
                    <el-form-item label="用户名" prop="username">
                        <el-input v-model="loginForm.username" />
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input v-model="loginForm.password" type="password" show-password
                            @keyup.enter="login(loginFormRef)" />
                        <!-- <el-checkbox v-model="loginForm.save_password" :value="true">
                            记住密码
                        </el-checkbox> -->
                    </el-form-item>
                    <el-form-item>
                        <el-button style="margin: auto;" type="success" size="default" plain :auto-insert-space="true"
                            @click="login(loginFormRef)">登录</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, type FormInstance } from 'element-plus';
import { loginApi } from '@/apis/userApis';
import { useUserStore } from '@/stores/user';

const router = useRouter();
const userStore = useUserStore();
const loginFormRef = ref<FormInstance>();

const loginForm = reactive({
    username: '',
    password: '',
})
const loginRules = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
    ],
}

async function login(formEl: FormInstance | undefined) {
    console.log('login');
    console.log(formEl);
    if (!formEl) return;
    formEl.validate(async (valid) => {
        if (valid) {
            const res = await loginApi(loginForm.username, loginForm.password);
            if (res.code == 0) {
                ElMessage.success('登录成功');
                userStore.setUser(res.data);
                router.push({ name: 'home' });
            }
        } else {
            ElMessage.error('请填写正确的用户名和密码');
            return false;
        }
    })
}

</script>
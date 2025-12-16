<template>
    <!-- <el-row>
        <el-col :span="3" :offset="6">
            <el-input v-model="searchVal" placeholder="搜索(文件名)" clearable size="default" @change="refreshFileList" />
        </el-col>
        <el-col :span="2" style="display:flex; align-items:center; justify-content: center;">
            <span>文件总数：{{ fileCount }}</span>
        </el-col>
        <el-col :span="1">
            <el-upload style="display: inline; margin-left: 12px;" v-loading.fullscreen.lock="fullscreenLoading"
                :show-file-list="false" :action="`${baseUrl}/api-file/files/`"
                :headers="userInfo ? { Authorization: `Bearer ${userInfo.access}` } : {}" name="file_path"
                :on-progress="openLoading" :on-success="afterUploadFile" :on-error="fileUploadError">
                <el-button color="#626aef" type="primary" text plain round size="default">上传文件</el-button>
            </el-upload>
        </el-col>
    </el-row> -->
    <el-row style="margin-top: 15px;">
        <el-col :span="12" :offset="6">
            <el-table :data="clipboardList" size="default" @sort-change="handleSortChange">
                <el-table-column sortable="custom" prop="title" label="名称"></el-table-column>
                <el-table-column sortable="custom" prop="created_at" label="创建时间" width="180" align="center" />
                <el-table-column sortable="custom" prop="updated_at" label="最后编辑时间" width="180" align="center" />
                <el-table-column prop="last_modified_user" label="最后编辑" width="180" align="center" />
                <el-table-column width="130">
                    <template #default="scope">
                        <el-button type="success" text plain
                            @click="goClipboardDetails(scope.row.share_id)">编辑</el-button>
                        <el-button type="danger" text plain @click="delClipboard(scope.row.id)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <el-row style="margin-top: 20px;">
        <el-col :span="16" :offset="4">
            <el-pagination style="justify-content: center" layout="total, prev, pager, next" :page-size="pageSize"
                :pager-count="5" :total="clipboardCount" @current-change="handleCurrentChange" />
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { useUserStore } from '@/stores/user';
import { getClipboardListApi, delClipboardListApi } from '@/apis/clipboardApis';
import type { Clipboard } from '@/interfaces';

const router = useRouter();

const userStore = useUserStore();
const userInfo = userStore.getUser();

const pageSize = ref(10);
const pageNum = ref(1);
const clipboardList = ref<Clipboard[]>([]);
const clipboardCount = ref(0);

function goClipboardDetails(shareID: string) {
    router.push({ name: 'clipboardIndex', params: { id: shareID } });
}

async function delClipboard(id: number) {
    ElMessageBox.confirm(
        '确认删除剪切板？',
        '警告',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    ).then(() => {
        delClipboardListApi(id).then(res => {
            console.log(res);
            if (res.code === 0) {
                ElMessage.success('删除成功');
                clipboardList.value = clipboardList.value.filter(item => item.id !== id);
                clipboardCount.value -= 1;
            }
        })
    }).catch(() => {
        ElMessage({
            type: 'info',
            message: '取消删除',
        })
    })
}

async function getClipboardList(value: number) {
    getClipboardListApi({ page_num: value }).then(res => {
        clipboardList.value = res.data.results;
        clipboardCount.value = res.data.count;
    })
}

async function handleCurrentChange(value: number) {
    getClipboardList(value);
}

onMounted(async () => {
    getClipboardList(1);
})

</script>
<script setup lang="ts">
import type { PortalApplicationUpsert, PortalStudentRecord } from '../../../../api/portal'
import type { SelectOption } from '../../../../api/common'

defineProps<{
  form: PortalApplicationUpsert
  student: PortalStudentRecord | null
  genderOptions: string[]
  ethnicGroupOptions: SelectOption[]
  politicalStatusOptions: SelectOption[]
  idTypeOptions: string[]
  profilePhotoAttachmentAccept: string
  isAttachmentUploading: (key: string) => boolean
  buildAttachmentUploadKey: (section: string, index: number | string, field: string) => string
  handleProfilePhotoUpload: (event: Event) => void | Promise<void>
}>()
</script>

<template>
  <section class="section-page">
    <div class="photo-card">
      <div class="photo-card__preview">
        <img v-if="form.profile?.profile_photo_url" :src="form.profile.profile_photo_url" alt="个人证件照片预览" />
        <div v-else class="photo-card__empty">请上传个人证件照片</div>
      </div>
      <div class="photo-card__content">
        <div>
          <strong><span class="required-mark">*</span>个人照片</strong>
          <p>建议使用身份证照片比例，作为报名资料随个人信息一并提交。</p>
        </div>
        <div class="upload-box">
          <input
            class="upload-box__input"
            type="file"
            :disabled="isAttachmentUploading(buildAttachmentUploadKey('profile', 0, 'photo'))"
            :accept="profilePhotoAttachmentAccept"
            @change="handleProfilePhotoUpload"
          />
          <small>{{ isAttachmentUploading(buildAttachmentUploadKey('profile', 0, 'photo')) ? '上传中...' : '支持 JPG/PNG/WEBP，单张不超过 1MB' }}</small>
        </div>
      </div>
    </div>

    <div class="section-grid">
      <label><span>姓名</span><input :value="student?.full_name || ''" disabled /></label>
      <label><span><span class="required-mark">*</span>姓名拼音</span><input v-model="form.profile!.full_name_pinyin" placeholder="请输入姓名拼音" /></label>
      <label><span><span class="required-mark">*</span>性别</span><select v-model="form.profile!.gender"><option value="">请选择</option><option v-for="item in genderOptions" :key="item" :value="item">{{ item }}</option></select></label>
      <label><span><span class="required-mark">*</span>民族</span><select v-model="form.profile!.ethnic_group"><option value="">请选择</option><option v-for="item in ethnicGroupOptions" :key="item.value" :value="item.value">{{ item.label }}</option></select></label>
      <label><span><span class="required-mark">*</span>政治面貌</span><select v-model="form.profile!.political_status"><option value="">请选择</option><option v-for="item in politicalStatusOptions" :key="item.value" :value="item.value">{{ item.label }}</option></select></label>
      <label><span>籍贯</span><input v-model="form.profile!.native_place" placeholder="请输入籍贯" /></label>
      <label><span>证件类型</span><select v-model="form.profile!.id_type"><option v-for="item in idTypeOptions" :key="item" :value="item">{{ item }}</option></select></label>
      <label><span>证件号码</span><input :value="student?.id_number || ''" disabled /></label>
      <label><span>邮箱</span><input :value="student?.email || ''" disabled /></label>
      <label><span>手机号码</span><input :value="student?.phone_number || ''" disabled /></label>
      <label><span><span class="required-mark">*</span>紧急联系人姓名</span><input v-model="form.profile!.emergency_contact_name" placeholder="请输入紧急联系人姓名" /></label>
      <label><span><span class="required-mark">*</span>紧急联系人手机</span><input v-model="form.profile!.emergency_contact_phone" placeholder="请输入紧急联系人手机" /></label>
      <label class="section-grid__full"><span><span class="required-mark">*</span>通讯地址</span><input v-model="form.profile!.mailing_address" placeholder="请输入通讯地址" /></label>
    </div>
  </section>
</template>

<style scoped>
.section-page {
  display: grid;
  gap: 20px;
}

.photo-card {
  display: grid;
  grid-template-columns: 180px minmax(0, 1fr);
  gap: 22px;
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(28, 70, 137, 0.08);
}

.photo-card__preview {
  width: 180px;
  height: 228px;
  overflow: hidden;
  border-radius: 22px;
  background: linear-gradient(180deg, #f2f7ff, #eef4ff);
  border: 1px solid rgba(145, 170, 209, 0.24);
  display: grid;
  place-items: center;
}

.photo-card__preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-card__empty {
  padding: 16px;
  color: #6c7f99;
  text-align: center;
}

.photo-card__content {
  display: grid;
  gap: 14px;
  align-content: start;
}

.photo-card__content strong {
  color: #173459;
  font-size: 24px;
}

.required-mark {
  margin-right: 4px;
  color: #e34d59;
  font-style: normal;
  font-weight: 700;
}

.photo-card__content p {
  margin: 8px 0 0;
  max-width: 380px;
  color: #657995;
  line-height: 1.7;
}

.upload-box {
  display: grid;
  gap: 8px;
}

.upload-box__input,
.section-grid input,
.section-grid select {
  width: 100%;
  min-height: 46px;
  padding: 10px 14px;
  border: 1px solid #d6e0ee;
  border-radius: 14px;
  background: #fff;
  color: #23344d;
  font: inherit;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 44px rgba(28, 70, 137, 0.08);
}

.section-grid label {
  display: grid;
  gap: 8px;
  color: #4b607d;
  font-size: 14px;
}

.section-grid__full {
  grid-column: 1 / -1;
}

@media (max-width: 1180px) {
  .section-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .photo-card,
  .section-grid {
    grid-template-columns: 1fr;
  }

  .photo-card__preview {
    width: 100%;
    max-width: 180px;
  }
}
</style>
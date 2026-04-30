<script setup lang="ts">
import type { PortalApplicationUpsert, PortalStudentRecord } from '../../../../api/portal'
import type { SelectOption } from '../../../../api/common'

const idCardCollageExampleImageUrl = '/images/id_example.jpg'

defineProps<{
  form: PortalApplicationUpsert
  student: PortalStudentRecord | null
  genderOptions: string[]
  ethnicGroupOptions: SelectOption[]
  politicalStatusOptions: SelectOption[]
  idTypeOptions: string[]
  profilePhotoAttachmentAccept: string
  idCardCollageAttachmentAccept: string
  isAttachmentUploading: (key: string) => boolean
  buildAttachmentUploadKey: (section: string, index: number | string, field: string) => string
  handleProfilePhotoUpload: (event: Event) => void | Promise<void>
  handleIdCardCollageUpload: (event: Event) => void | Promise<void>
}>()
</script>

<template>
  <section class="section-page">
    <div class="upload-panel-grid">
      <div class="upload-panel upload-panel--photo">
        <div class="upload-panel__preview upload-panel__preview--photo">
          <div v-if="form.profile?.profile_photo_url" class="upload-panel__media">
            <img :src="form.profile.profile_photo_url" alt="个人证件照片预览" />
          </div>
          <div v-else class="upload-panel__empty">请上传个人证件照片</div>
        </div>
        <div class="upload-panel__content">
          <div>
            <strong><span class="required-mark">*</span>个人照片</strong>
            <p>纯色背景的近期免冠证件照</p>
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

      <div class="upload-panel upload-panel--collage">
        <div class="upload-panel__preview upload-panel__preview--contain upload-panel__preview--collage">
          <div v-if="form.profile?.id_card_collage_url" class="upload-panel__media">
            <img :src="form.profile.id_card_collage_url" alt="身份证拼图预览" />
          </div>
          <div v-else class="upload-panel__empty">请上传身份证拼图</div>
        </div>
        <div class="upload-panel__content">
          <div>
            <strong><span class="required-mark">*</span>身份证拼图</strong>
            <p>请上传一张拼图，上半部分为身份证正面，下半部分为身份证背面。</p>
          </div>
          <div class="upload-box">
            <input
              class="upload-box__input"
              type="file"
              :disabled="isAttachmentUploading(buildAttachmentUploadKey('profile', 0, 'id-card-collage'))"
              :accept="idCardCollageAttachmentAccept"
              @change="handleIdCardCollageUpload"
            />
            <small>{{ isAttachmentUploading(buildAttachmentUploadKey('profile', 0, 'id-card-collage')) ? '上传中...' : '仅支持 JPG/JPEG，单张不超过 5MB' }}</small>
          </div>
        </div>
      </div>

      <div class="upload-panel upload-panel--sample">
        <div class="upload-panel__preview upload-panel__preview--contain upload-panel__preview--sample">
          <div class="upload-panel__media">
            <img :src="idCardCollageExampleImageUrl" alt="身份证拼图样例" />
          </div>
        </div>
        <div class="upload-panel__content">
          <div>
            <strong>示例图</strong>
            <p>请参考样例拼接身份证正反面照片后再上传，保持正面在上、背面在下。</p>
          </div>
          <div class="upload-box upload-box--hint">
            <small>当前展示的是系统内置样例图，仅作拼图格式参考，不会随报名表一同提交。</small>
          </div>
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

.upload-panel-grid {
  display: grid;
  grid-template-columns: minmax(0, 8fr) minmax(0, 8fr) minmax(0, 4fr);
  gap: 14px;
  align-items: stretch;
}

.upload-panel {
  display: grid;
  grid-template-rows: 168px minmax(0, 1fr);
  gap: 14px;
  padding: 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 12px 28px rgba(28, 70, 137, 0.08);
  height: 100%;
}

.upload-panel__preview {
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 16px;
  background: linear-gradient(180deg, #f2f7ff, #eef4ff);
  border: 1px solid rgba(145, 170, 209, 0.24);
  display: grid;
  place-items: center;
  padding: 10px;
  box-sizing: border-box;
}

.upload-panel__media {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.upload-panel__preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.upload-panel__preview--contain img {
  object-fit: contain;
  background: #f7f9fd;
}

.upload-panel__preview--sample {
  border-style: dashed;
  border-color: rgba(213, 172, 70, 0.45);
  background: linear-gradient(180deg, #fff9e8, #fffdf6);
}

.upload-panel__empty {
  padding: 12px;
  color: #6c7f99;
  text-align: center;
  font-size: 13px;
}

.upload-panel__content {
  display: grid;
  grid-template-rows: auto auto;
  gap: 10px;
  align-content: start;
}

.upload-panel__content strong {
  color: #173459;
  font-size: 18px;
}

.required-mark {
  margin-right: 4px;
  color: #e34d59;
  font-style: normal;
  font-weight: 700;
}

.upload-panel__content p {
  margin: 8px 0 0;
  color: #657995;
  font-size: 13px;
  line-height: 1.55;
}

.upload-box {
  display: grid;
  gap: 6px;
}

.upload-box--hint {
  align-content: end;
}

.upload-box__input,
.section-grid input,
.section-grid select {
  width: 100%;
  min-height: 40px;
  padding: 8px 12px;
  border: 1px solid #d6e0ee;
  border-radius: 12px;
  background: #fff;
  color: #23344d;
  font: inherit;
}

.upload-box small {
  font-size: 12px;
  line-height: 1.4;
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
  .upload-panel-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .section-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .upload-panel--sample {
    grid-column: 1 / -1;
  }
}

@media (max-width: 720px) {
  .upload-panel-grid,
  .section-grid {
    grid-template-columns: 1fr;
  }

  .upload-panel {
    grid-template-rows: 156px minmax(0, 1fr);
  }
}
</style>
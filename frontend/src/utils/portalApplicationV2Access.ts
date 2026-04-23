import type { Router } from 'vue-router'

import { getPortalPublicConfig } from '../api/portal'
import { showPortalAlert, showPortalAlertHtml } from './portalAlerts'

const DEFAULT_BLOCK_MESSAGE = '4月30日（周四）20点之前开放，敬请期待'
const PORTAL_APPLICATION_UPCOMING_TITLE = '在线申请即将开启'
const PORTAL_APPLICATION_UPCOMING_MESSAGE = [
  '系统将于4月30日（周四）20点之前开放申请，敬请期待。',
  '您亦可将个人简历发送至邮箱：<a href="mailto:admissions@pjlab.org.cn">admissions@pjlab.org.cn</a>',
].join('<br />')

export async function ensurePortalApplicationV2Available(): Promise<boolean> {
  try {
    const response = await getPortalPublicConfig()
    if (!response.data.portal_application_v2_blocked) {
      return true
    }

    const blockMessage = response.data.portal_application_v2_block_message || DEFAULT_BLOCK_MESSAGE
    if (blockMessage === DEFAULT_BLOCK_MESSAGE) {
      await showPortalAlertHtml(PORTAL_APPLICATION_UPCOMING_MESSAGE, PORTAL_APPLICATION_UPCOMING_TITLE, 'warning')
    } else {
      await showPortalAlert(blockMessage, PORTAL_APPLICATION_UPCOMING_TITLE, 'warning')
    }
    return false
  } catch {
    await showPortalAlert('在线申报入口暂时不可用，请稍后重试', '在线申报', 'warning')
    return false
  }
}

export async function openPortalApplicationV2(router: Router): Promise<boolean> {
  const allowed = await ensurePortalApplicationV2Available()
  if (!allowed) {
    return false
  }

  await router.push('/portal/applicationv2')
  return true
}
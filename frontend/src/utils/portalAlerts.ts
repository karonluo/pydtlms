import axios from 'axios'

export type PortalAlertType = 'success' | 'warning' | 'error'

const PORTAL_ALERT_STYLE_ID = 'portal-alert-styles'

function ensurePortalAlertStyles() {
  if (document.getElementById(PORTAL_ALERT_STYLE_ID)) {
    return
  }

  const style = document.createElement('style')
  style.id = PORTAL_ALERT_STYLE_ID
  style.textContent = `
    .portal-alert-overlay {
      position: fixed;
      inset: 0;
      z-index: 5000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      background: rgba(6, 28, 62, 0.42);
    }

    .portal-alert-dialog {
      width: min(420px, calc(100vw - 32px));
      border-radius: 18px;
      background: #ffffff;
      box-shadow: 0 28px 72px rgba(8, 42, 102, 0.24);
      overflow: hidden;
      border: 1px solid rgba(213, 224, 240, 0.92);
      font-family: 'Aptos', 'Microsoft YaHei UI', 'PingFang SC', sans-serif;
    }

    .portal-alert-dialog__header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 18px 20px 12px;
    }

    .portal-alert-dialog__title-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }

    .portal-alert-dialog__badge {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex: 0 0 auto;
    }

    .portal-alert-dialog__badge--success {
      background: #22a06b;
    }

    .portal-alert-dialog__badge--warning {
      background: #e5a127;
    }

    .portal-alert-dialog__badge--error {
      background: #de4c4c;
    }

    .portal-alert-dialog__title {
      color: #173459;
      font-size: 18px;
      font-weight: 700;
      line-height: 1.3;
    }

    .portal-alert-dialog__close {
      border: none;
      background: transparent;
      color: #7a8da8;
      font-size: 18px;
      line-height: 1;
      cursor: pointer;
    }

    .portal-alert-dialog__body {
      padding: 0 20px 20px;
      color: #455a78;
      font-size: 14px;
      line-height: 1.7;
      white-space: pre-wrap;
      word-break: break-word;
    }

    .portal-alert-dialog__actions {
      display: flex;
      justify-content: flex-end;
      padding: 0 20px 20px;
    }

    .portal-alert-dialog__confirm {
      min-width: 92px;
      min-height: 38px;
      padding: 0 18px;
      border: none;
      border-radius: 10px;
      background: linear-gradient(135deg, #1f73d8, #1b58b3);
      color: #fff;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
    }
  `
  document.head.appendChild(style)
}

export async function showPortalAlert(message: string, title: string, type: PortalAlertType = 'warning') {
  ensurePortalAlertStyles()

  await new Promise<void>((resolve) => {
    const overlay = document.createElement('div')
    overlay.className = 'portal-alert-overlay'

    const dialog = document.createElement('div')
    dialog.className = 'portal-alert-dialog'
    dialog.setAttribute('role', 'dialog')
    dialog.setAttribute('aria-modal', 'true')
    dialog.setAttribute('aria-label', title)

    const header = document.createElement('div')
    header.className = 'portal-alert-dialog__header'

    const titleWrap = document.createElement('div')
    titleWrap.className = 'portal-alert-dialog__title-wrap'

    const badge = document.createElement('span')
    badge.className = `portal-alert-dialog__badge portal-alert-dialog__badge--${type}`

    const titleNode = document.createElement('strong')
    titleNode.className = 'portal-alert-dialog__title'
    titleNode.textContent = title

    const closeButton = document.createElement('button')
    closeButton.type = 'button'
    closeButton.className = 'portal-alert-dialog__close'
    closeButton.setAttribute('aria-label', '关闭提示')
    closeButton.textContent = '×'

    const body = document.createElement('div')
    body.className = 'portal-alert-dialog__body'
    body.textContent = message

    const actions = document.createElement('div')
    actions.className = 'portal-alert-dialog__actions'

    const confirmButton = document.createElement('button')
    confirmButton.type = 'button'
    confirmButton.className = 'portal-alert-dialog__confirm'
    confirmButton.textContent = '确定'

    const cleanup = () => {
      document.removeEventListener('keydown', handleKeydown)
      overlay.remove()
      resolve()
    }

    const handleKeydown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' || event.key === 'Enter') {
        event.preventDefault()
        cleanup()
      }
    }

    closeButton.addEventListener('click', cleanup)
    confirmButton.addEventListener('click', cleanup)
    overlay.addEventListener('click', (event) => {
      if (event.target === overlay) {
        cleanup()
      }
    })

    document.addEventListener('keydown', handleKeydown)

    titleWrap.appendChild(badge)
    titleWrap.appendChild(titleNode)
    header.appendChild(titleWrap)
    header.appendChild(closeButton)
    actions.appendChild(confirmButton)

    dialog.appendChild(header)
    dialog.appendChild(body)
    dialog.appendChild(actions)
    overlay.appendChild(dialog)
    document.body.appendChild(overlay)

    confirmButton.focus()
  })
}

export function resolveRequestError(error: unknown, fallback: string) {
  if (!axios.isAxiosError(error)) {
    return fallback
  }

  const detail = error.response?.data?.detail
  if (typeof detail === 'string' && detail.trim()) {
    return detail
  }

  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map((item) => (typeof item === 'string' ? item : String(item?.msg || item))).join('；')
  }

  return fallback
}
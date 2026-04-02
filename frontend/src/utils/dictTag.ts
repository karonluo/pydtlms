export type DictColorMap = Record<string, string>

export function buildDictColorMap(options: Array<{ label: string; value: string; color_type?: string | null }>) {
  const colorMap: DictColorMap = {}
  options.forEach((item) => {
    colorMap[item.value] = item.color_type || 'info'
    if (item.label !== item.value) {
      colorMap[item.label] = item.color_type || 'info'
    }
  })
  return colorMap
}

export function resolveDictTagType(status: string, ...maps: Array<DictColorMap | undefined>) {
  for (const currentMap of maps) {
    if (currentMap && currentMap[status]) {
      return currentMap[status]
    }
  }
  return 'info'
}
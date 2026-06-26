## 元数据

- **类型**: Workflow
- **分类**: Frontend & UI
- **适用场景**: Build mobile apps with React Native and Expo — navigation, platform-specific code, performance, and native modules.
- **上游来源**: [react-native-patterns](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/react-native-patterns)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# React Native Patterns

Build production-quality mobile apps with React Native and Expo.

## Project Setup

**Expo (recommended for most projects):**
```bash
npx create-expo-app@latest my-app
cd my-app
npx expo start
```

**Bare React Native (when you need full native control):**
```bash
npx @react-native-community/cli init MyApp
```

Use Expo unless you need a custom native module that Expo doesn't support.

## Navigation

Use `expo-router` (file-based routing) or `@react-navigation/native`:

```
app/
├── _layout.tsx        # Root layout (tabs, stack, drawer)
├── index.tsx          # Home screen
├── (tabs)/
│   ├── _layout.tsx    # Tab navigator
│   ├── home.tsx
│   ├── profile.tsx
│   └── settings.tsx
└── [id].tsx           # Dynamic route
```

## Platform-Specific Code

```typescript
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1 },
    android: { elevation: 4 },
  }),
});
```

For larger differences, use platform-specific files:
- `Component.ios.tsx`
- `Component.android.tsx`

## Styling

Use `StyleSheet.create` for performance (styles are sent to native once):

```typescript
const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  title: { fontSize: 24, fontWeight: '700' },
});
```

For a Tailwind-like experience, use `nativewind`:
```tsx
<View className="flex-1 p-4">
  <Text className="text-2xl font-bold">Hello</Text>
</View>
```

## Performance

**FlatList over ScrollView** for long lists:
```tsx
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <ItemRow item={item} />}
  initialNumToRender={10}
  maxToRenderPerBatch={5}
  windowSize={5}
/>
```

**Memoize expensive components:**
```tsx
const ItemRow = React.memo(({ item }: { item: Item }) => (
  <View><Text>{item.name}</Text></View>
));
```

**Avoid:**
- Inline styles (creates new objects every render)
- Anonymous functions in `renderItem`
- Large images without caching (`expo-image` handles this)

## Common Libraries

| Need | Library |
|------|---------|
| Navigation | `expo-router` or `@react-navigation/native` |
| State | `zustand`, `jotai`, or React context |
| Data fetching | `@tanstack/react-query` |
| Images | `expo-image` |
| Icons | `@expo/vector-icons` |
| Storage | `expo-secure-store` (sensitive), `@react-native-async-storage/async-storage` (general) |
| Animations | `react-native-reanimated` |
| Gestures | `react-native-gesture-handler` |
| Forms | `react-hook-form` + `zod` |

## Tips

- Test on both iOS and Android from the start, not at the end
- Use `expo-dev-client` for custom native modules with Expo
- Handle safe areas with `react-native-safe-area-context`
- Always handle keyboard avoidance for forms (`KeyboardAvoidingView`)
- Use `expo-updates` for OTA updates in production

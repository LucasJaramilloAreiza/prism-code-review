import "./globals.css";
export const metadata = { title: "PRism", description: "Multi-agent code review" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en">
<body>{children}</body>
</html>);
}

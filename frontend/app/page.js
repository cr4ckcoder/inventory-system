import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <div className="flex h-screen items-center justify-center">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">ShadCN ✅ is Working!</h1>
        <Button>Click Me</Button>
      </div>
    </div>
  );
}
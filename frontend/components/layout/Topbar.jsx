"use client";

import { Menu, User } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Topbar({ toggleSidebar }) {
  return (
    <header className="flex items-center justify-between px-4 py-3 border-b bg-white">
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" onClick={toggleSidebar} className="md:hidden">
          <Menu className="h-5 w-5" />
        </Button>
        <h1 className="text-xl font-semibold text-gray-800">Dashboard</h1>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-sm text-gray-700">
          <User className="w-4 h-4" /> Admin
        </div>
      </div>
    </header>
  );
}

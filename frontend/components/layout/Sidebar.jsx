"use client";

import { Home, Package, ShoppingCart, Users, LogOut } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

const menuItems = [
  { name: "Dashboard", icon: Home, href: "/dashboard" },
  { name: "Products", icon: Package, href: "/dashboard/products" },
  { name: "Categories", icon: Package, href: "/dashboard/categories" },
  { name: "Inventory", icon: ShoppingCart, href: "/dashboard/inventory" },
  { name: "Transfers", icon: Package, href: "/dashboard/transfers" },
  { name: "Users", icon: Users, href: "/dashboard/users" },
];

export default function Sidebar() {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <div className="flex flex-col h-screen w-64 bg-white border-r shadow-sm">
      <div className="p-6 text-2xl font-bold">CIS</div>
      <nav className="flex-1 px-4 space-y-2">
        {menuItems.map(({ name, icon: Icon, href }) => (
          <Link
            key={name}
            href={href}
            className="flex items-center gap-3 px-3 py-2 rounded-md text-gray-700 hover:bg-gray-100 hover:text-gray-900"
          >
            <Icon className="h-5 w-5" />
            {name}
          </Link>
        ))}
      </nav>
      <div className="p-4">
        <Button variant="destructive" className="w-full" onClick={handleLogout}>
          <LogOut className="w-4 h-4 mr-2" />
          Logout
        </Button>
      </div>
    </div>
  );
}

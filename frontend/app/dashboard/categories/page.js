"use client";

import { useEffect, useState } from "react";
import { getCategories, createCategory } from "@/lib/api";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

export default function CategoriesPage() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [categoryName, setCategoryName] = useState("");

  // Fetch all categories
  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getCategories();
        setCategories(data);
      } catch (err) {
        console.error("Failed to fetch categories:", err);
        toast.error("Error loading categories");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // Create a new category
  async function handleCreateCategory(e) {
    e.preventDefault();
    try {
      const newCategory = await createCategory({ category_name: categoryName });
      toast.success("Category created successfully!");
      setCategories((prev) => [...prev, newCategory]);
      setCategoryName("");
      setOpen(false);
    } catch (err) {
      console.error("Failed to create category:", err);
      toast.error("Error creating category");
    }
  }

  if (loading) return <p className="text-gray-500">Loading categories...</p>;

  return (
    <div className="space-y-6">
      {/* Header with Add Button */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold">Categories</h2>

        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button>Add Category</Button>
          </DialogTrigger>

          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Create New Category</DialogTitle>
              <DialogDescription>Enter a unique name for the category.</DialogDescription>
            </DialogHeader>

            <form onSubmit={handleCreateCategory} className="space-y-4 mt-2">
              <div>
                <label className="block text-sm font-medium mb-1">Category Name</label>
                <Input
                  type="text"
                  placeholder="e.g. Beverages, Clothing"
                  value={categoryName}
                  onChange={(e) => setCategoryName(e.target.value)}
                  required
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <Button type="button" variant="outline" onClick={() => setOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit">Create</Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Category List */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {categories.length > 0 ? (
          categories.map((cat) => (
            <Card key={cat.category_id} className="p-4 shadow-sm border">
              <h3 className="text-lg font-medium">{cat.category_name}</h3>
            </Card>
          ))
        ) : (
          <p className="text-gray-500 italic">No categories found.</p>
        )}
      </div>
    </div>
  );
}

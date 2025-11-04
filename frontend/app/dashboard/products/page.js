"use client";

import { useEffect, useState } from "react";
import { getProducts, createProduct, getCategories } from "@/lib/api";
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
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";


export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [categories, setCategories] = useState([]);
  const [formData, setFormData] = useState({
    style_name: "",
    description: "",
    category_id: "",
  });

  useEffect(() => {
  async function fetchCategories() {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (err) {
      console.error("Failed to load categories:", err);
    }
  }
  fetchCategories();
}, []);

  // Fetch existing products
  useEffect(() => {
    async function fetchProducts() {
      try {
        const data = await getProducts();
        setProducts(data);
      } catch (err) {
        console.error("Failed to fetch products:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchProducts();
  }, []);

  // Handle form submission
  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const newProduct = await createProduct(formData);
      toast.success("Product created successfully!");
      setProducts((prev) => [...prev, newProduct]);
      setOpen(false);
      setFormData({ style_name: "", description: "", category_id: "" });
    } catch (err) {
      console.error("Failed to create product:", err);
      toast.error("Error creating product");
    }
  }

  if (loading) return <p className="text-gray-500">Loading products...</p>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-semibold">Products</h2>

        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button>Add Product</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Create New Product</DialogTitle>
              <DialogDescription>Enter details for your new product.</DialogDescription>
            </DialogHeader>

            <form onSubmit={handleSubmit} className="space-y-4 mt-2">
              <div>
                <label className="block text-sm font-medium mb-1">Style Name</label>
                <Input
                  type="text"
                  value={formData.style_name}
                  onChange={(e) => setFormData({ ...formData, style_name: e.target.value })}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Description</label>
                <Textarea
                  rows={3}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              <div>
            <label className="block text-sm font-medium mb-1">Category</label>
            <Select
                value={formData.category_id}
                onValueChange={(value) => setFormData({ ...formData, category_id: value })}
            >
                <SelectTrigger>
                <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                {categories.map((cat) => (
                    <SelectItem key={cat.category_id} value={cat.category_id}>
                    {cat.category_name}
                    </SelectItem>
                ))}
                </SelectContent>
            </Select>
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

      {/* Product cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {products.length > 0 ? (
          products.map((product) => (
            <Card key={product.product_id} className="p-4 shadow-sm border">
              <h3 className="text-lg font-medium">{product.style_name}</h3>
              <p className="text-sm text-gray-500 mt-1">{product.description}</p>
            </Card>
          ))
        ) : (
          <p className="text-gray-500 italic">No products found.</p>
        )}
      </div>
    </div>
  );
}

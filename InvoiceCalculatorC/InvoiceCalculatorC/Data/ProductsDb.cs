using InvoiceCalculatorC.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceCalculatorC.Data;

public class ProductsDb : DbContext
{
    public ProductsDb(DbContextOptions<ProductsDb> options) : base(options)
    {
        
    }
    
    public DbSet<Product>  Products => Set<Product>();
}
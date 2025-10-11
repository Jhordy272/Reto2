using System.ComponentModel.DataAnnotations.Schema;

namespace InvoiceCalculatorC.Models;

[Table("products")] // Especifica el nombre exacto de la tabla
public class Product
{
    public long id { get; set; }
    public string name { get; set; }
    public string description { get; set; }
    public int stock { get; set; }
    public double price { get; set; }
}
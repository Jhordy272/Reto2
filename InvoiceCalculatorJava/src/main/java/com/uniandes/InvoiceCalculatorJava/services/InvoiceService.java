package com.uniandes.InvoiceCalculatorJava.services;

import com.uniandes.InvoiceCalculatorJava.dto.InvoiceItemRequest;
import com.uniandes.InvoiceCalculatorJava.dto.InvoiceItemResponse;
import com.uniandes.InvoiceCalculatorJava.dto.InvoiceRequest;
import com.uniandes.InvoiceCalculatorJava.dto.InvoiceResponse;
import com.uniandes.InvoiceCalculatorJava.models.Product;
import com.uniandes.InvoiceCalculatorJava.repositories.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class InvoiceService {

    @Autowired
    private ProductRepository productRepository;

    public InvoiceResponse calculateInvoice(InvoiceRequest request) {
        List<InvoiceItemResponse> itemResponses = new ArrayList<>();
        double total = 0.0;

        for (InvoiceItemRequest item : request.getItems()) {
            Product product = productRepository.findById(item.getProductId())
                    .orElseThrow(() -> new RuntimeException("Product not found with id: " + item.getProductId()));

            if (product.getStock() < item.getQuantity()) {
                throw new RuntimeException("Insufficient stock for product: " + product.getName());
            }

            double subtotal = product.getPrice() * item.getQuantity();
            total += subtotal;

            InvoiceItemResponse itemResponse = new InvoiceItemResponse(
                    product.getId(),
                    product.getName(),
                    item.getQuantity(),
                    product.getPrice(),
                    subtotal
            );

            itemResponses.add(itemResponse);
        }

        return new InvoiceResponse(itemResponses, total);
    }
}

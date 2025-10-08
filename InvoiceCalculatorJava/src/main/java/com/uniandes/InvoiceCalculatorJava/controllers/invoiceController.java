package com.uniandes.InvoiceCalculatorJava.controllers;

import com.uniandes.InvoiceCalculatorJava.dto.InvoiceRequest;
import com.uniandes.InvoiceCalculatorJava.dto.InvoiceResponse;
import com.uniandes.InvoiceCalculatorJava.services.InvoiceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("invoice")
public class invoiceController {

    @Autowired
    private InvoiceService invoiceService;

    @PostMapping("/calculate")
    public ResponseEntity<InvoiceResponse> calculateInvoice(@RequestBody InvoiceRequest request) {
        try {
            InvoiceResponse response = invoiceService.calculateInvoice(request);
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().build();
        }
    }
}

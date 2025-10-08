package com.uniandes.InvoiceCalculatorJava.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class InvoiceItemRequest {

    private Long productId;
    private Integer quantity;
}

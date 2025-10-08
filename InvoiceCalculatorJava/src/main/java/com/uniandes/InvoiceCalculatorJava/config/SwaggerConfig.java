package com.uniandes.InvoiceCalculatorJava.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;

@Configuration
public class SwaggerConfig {
    
    @Bean
    public OpenAPI invoiceCalculatorJavaOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Invoice Calculator Java")
                        .description("Invoice Calculator Java")
                        .version("v1.0.0")
                        .license(new License()
                                .name("MIT License")
                                .url("https://opensource.org/licenses/MIT")));
    }
}
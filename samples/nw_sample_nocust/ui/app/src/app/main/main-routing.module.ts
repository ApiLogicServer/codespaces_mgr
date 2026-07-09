import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MainComponent } from './main.component';

export const routes: Routes = [
  {
    path: '', component: MainComponent,
    children: [
        { path: '', redirectTo: 'home', pathMatch: 'full' },
        { path: 'about', loadChildren: () => import('./about/about.module').then(m => m.AboutModule) },
        { path: 'home', loadChildren: () => import('./home/home.module').then(m => m.HomeModule) },
        { path: 'settings', loadChildren: () => import('./settings/settings.module').then(m => m.SettingsModule) },
      
    
        { path: 'Category', loadChildren: () => import('./Category/Category.module').then(m => m.CategoryModule) },
    
        { path: 'Customer', loadChildren: () => import('./Customer/Customer.module').then(m => m.CustomerModule) },
    
        { path: 'CustomerDemographic', loadChildren: () => import('./CustomerDemographic/CustomerDemographic.module').then(m => m.CustomerDemographicModule) },
    
        { path: 'Department', loadChildren: () => import('./Department/Department.module').then(m => m.DepartmentModule) },
    
        { path: 'Employee', loadChildren: () => import('./Employee/Employee.module').then(m => m.EmployeeModule) },
    
        { path: 'EmployeeAudit', loadChildren: () => import('./EmployeeAudit/EmployeeAudit.module').then(m => m.EmployeeAuditModule) },
    
        { path: 'EmployeeTerritory', loadChildren: () => import('./EmployeeTerritory/EmployeeTerritory.module').then(m => m.EmployeeTerritoryModule) },
    
        { path: 'Location', loadChildren: () => import('./Location/Location.module').then(m => m.LocationModule) },
    
        { path: 'Order', loadChildren: () => import('./Order/Order.module').then(m => m.OrderModule) },
    
        { path: 'OrderDetail', loadChildren: () => import('./OrderDetail/OrderDetail.module').then(m => m.OrderDetailModule) },
    
        { path: 'Product', loadChildren: () => import('./Product/Product.module').then(m => m.ProductModule) },
    
        { path: 'Region', loadChildren: () => import('./Region/Region.module').then(m => m.RegionModule) },
    
        { path: 'SampleDBVersion', loadChildren: () => import('./SampleDBVersion/SampleDBVersion.module').then(m => m.SampleDBVersionModule) },
    
        { path: 'Shipper', loadChildren: () => import('./Shipper/Shipper.module').then(m => m.ShipperModule) },
    
        { path: 'Supplier', loadChildren: () => import('./Supplier/Supplier.module').then(m => m.SupplierModule) },
    
        { path: 'Territory', loadChildren: () => import('./Territory/Territory.module').then(m => m.TerritoryModule) },
    
        { path: 'Union', loadChildren: () => import('./Union/Union.module').then(m => m.UnionModule) },
    
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule { }
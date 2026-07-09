import { MenuRootItem } from 'ontimize-web-ngx';

import { CategoryCardComponent } from './Category-card/Category-card.component';

import { CustomerCardComponent } from './Customer-card/Customer-card.component';

import { CustomerDemographicCardComponent } from './CustomerDemographic-card/CustomerDemographic-card.component';

import { DepartmentCardComponent } from './Department-card/Department-card.component';

import { EmployeeCardComponent } from './Employee-card/Employee-card.component';

import { EmployeeAuditCardComponent } from './EmployeeAudit-card/EmployeeAudit-card.component';

import { EmployeeTerritoryCardComponent } from './EmployeeTerritory-card/EmployeeTerritory-card.component';

import { LocationCardComponent } from './Location-card/Location-card.component';

import { OrderCardComponent } from './Order-card/Order-card.component';

import { OrderDetailCardComponent } from './OrderDetail-card/OrderDetail-card.component';

import { ProductCardComponent } from './Product-card/Product-card.component';

import { RegionCardComponent } from './Region-card/Region-card.component';

import { SampleDBVersionCardComponent } from './SampleDBVersion-card/SampleDBVersion-card.component';

import { ShipperCardComponent } from './Shipper-card/Shipper-card.component';

import { SupplierCardComponent } from './Supplier-card/Supplier-card.component';

import { TerritoryCardComponent } from './Territory-card/Territory-card.component';

import { UnionCardComponent } from './Union-card/Union-card.component';


export const MENU_CONFIG: MenuRootItem[] = [
    { id: 'home', name: 'HOME', icon: 'home', route: '/main/home' },
    
    {
    id: 'data', name: ' data', icon: 'remove_red_eye', opened: true,
    items: [
    
        { id: 'Category', name: 'CATEGORY', icon: 'view_list', route: '/main/Category' }
    
        ,{ id: 'Customer', name: 'CUSTOMER', icon: 'view_list', route: '/main/Customer' }
    
        ,{ id: 'CustomerDemographic', name: 'CUSTOMERDEMOGRAPHIC', icon: 'view_list', route: '/main/CustomerDemographic' }
    
        ,{ id: 'Department', name: 'DEPARTMENT', icon: 'view_list', route: '/main/Department' }
    
        ,{ id: 'Employee', name: 'EMPLOYEE', icon: 'view_list', route: '/main/Employee' }
    
        ,{ id: 'EmployeeAudit', name: 'EMPLOYEEAUDIT', icon: 'view_list', route: '/main/EmployeeAudit' }
    
        ,{ id: 'EmployeeTerritory', name: 'EMPLOYEETERRITORY', icon: 'view_list', route: '/main/EmployeeTerritory' }
    
        ,{ id: 'Location', name: 'LOCATION', icon: 'view_list', route: '/main/Location' }
    
        ,{ id: 'Order', name: 'ORDER', icon: 'view_list', route: '/main/Order' }
    
        ,{ id: 'OrderDetail', name: 'ORDERDETAIL', icon: 'view_list', route: '/main/OrderDetail' }
    
        ,{ id: 'Product', name: 'PRODUCT', icon: 'view_list', route: '/main/Product' }
    
        ,{ id: 'Region', name: 'REGION', icon: 'view_list', route: '/main/Region' }
    
        ,{ id: 'SampleDBVersion', name: 'SAMPLEDBVERSION', icon: 'view_list', route: '/main/SampleDBVersion' }
    
        ,{ id: 'Shipper', name: 'SHIPPER', icon: 'view_list', route: '/main/Shipper' }
    
        ,{ id: 'Supplier', name: 'SUPPLIER', icon: 'view_list', route: '/main/Supplier' }
    
        ,{ id: 'Territory', name: 'TERRITORY', icon: 'view_list', route: '/main/Territory' }
    
        ,{ id: 'Union', name: 'UNION', icon: 'view_list', route: '/main/Union' }
    
    ] 
},
    
    { id: 'settings', name: 'Settings', icon: 'settings', route: '/main/settings'}
    ,{ id: 'about', name: 'About', icon: 'info', route: '/main/about'}
    ,{ id: 'logout', name: 'LOGOUT', route: '/login', icon: 'power_settings_new', confirm: 'yes' }
];

export const MENU_COMPONENTS = [

    CategoryCardComponent

    ,CustomerCardComponent

    ,CustomerDemographicCardComponent

    ,DepartmentCardComponent

    ,EmployeeCardComponent

    ,EmployeeAuditCardComponent

    ,EmployeeTerritoryCardComponent

    ,LocationCardComponent

    ,OrderCardComponent

    ,OrderDetailCardComponent

    ,ProductCardComponent

    ,RegionCardComponent

    ,SampleDBVersionCardComponent

    ,ShipperCardComponent

    ,SupplierCardComponent

    ,TerritoryCardComponent

    ,UnionCardComponent

];
<?= $this->extend('base_ui/home'); ?>
<?= $this->section('menu'); ?>
<div class="sidebar-menu">
    <ul class="menu">
        <li class="sidebar-title">Menu</li>

        <li class="sidebar-item active ">
            <a href="index.html" class='sidebar-link'>
                <i class="bi bi-grid-fill"></i>
                <span>Dashboard</span>
            </a>
        </li>

        <li class="sidebar-item  has-sub">
            <a href="#" class='sidebar-link'>
                <i class="bi bi-stack"></i>
                <span>Components</span>
            </a>
            <ul class="submenu ">
                <li class="submenu-item ">
                    <a href="component-alert.html">Alert</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-badge.html">Badge</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-breadcrumb.html">Breadcrumb</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-button.html">Button</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-card.html">Card</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-carousel.html">Carousel</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-dropdown.html">Dropdown</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-list-group.html">List Group</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-modal.html">Modal</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-navs.html">Navs</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-pagination.html">Pagination</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-progress.html">Progress</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-spinner.html">Spinner</a>
                </li>
                <li class="submenu-item ">
                    <a href="component-tooltip.html">Tooltip</a>
                </li>
            </ul>
        </li>

        <li class="sidebar-item  has-sub">
            <a href="#" class='sidebar-link'>
                <i class="bi bi-collection-fill"></i>
                <span>Extra Components</span>
            </a>
            <ul class="submenu ">
                <li class="submenu-item ">
                    <a href="extra-component-avatar.html">Avatar</a>
                </li>
                <li class="submenu-item ">
                    <a href="extra-component-sweetalert.html">Sweet Alert</a>
                </li>
                <li class="submenu-item ">
                    <a href="extra-component-toastify.html">Toastify</a>
                </li>
                <li class="submenu-item ">
                    <a href="extra-component-rating.html">Rating</a>
                </li>
                <li class="submenu-item ">
                    <a href="extra-component-divider.html">Divider</a>
                </li>
            </ul>
        </li>

        <li class="sidebar-item  has-sub">
            <a href="#" class='sidebar-link'>
                <i class="bi bi-grid-1x2-fill"></i>
                <span>Layouts</span>
            </a>
            <ul class="submenu ">
                <li class="submenu-item ">
                    <a href="layout-default.html">Default Layout</a>
                </li>
                <li class="submenu-item ">
                    <a href="layout-vertical-1-column.html">1 Column</a>
                </li>
                <li class="submenu-item ">
                    <a href="layout-vertical-navbar.html">Vertical Navbar</a>
                </li>
                <li class="submenu-item ">
                    <a href="layout-rtl.html">RTL Layout</a>
                </li>
                <li class="submenu-item ">
                    <a href="layout-horizontal.html">Horizontal Menu</a>
                </li>
            </ul>
        </li>

        <li class="sidebar-title">Forms &amp; Tables</li>

        <li class="sidebar-item  has-sub">
            <a href="#" class='sidebar-link'>
                <i class="bi bi-hexagon-fill"></i>
                <span>Form Elements</span>
            </a>
            <ul class="submenu ">
                <li class="submenu-item ">
                    <a href="form-element-input.html">Input</a>
                </li>
                <li class="submenu-item ">
                    <a href="form-element-input-group.html">Input Group</a>
                </li>
                <li class="submenu-item ">
                    <a href="form-element-select.html">Select</a>
                </li>
                <li class="submenu-item ">
                    <a href="form-element-radio.html">Radio</a>
                </li>
                <li class="submenu-item ">
                    <a href="form-element-checkbox.html">Checkbox</a>
                </li>
                <li class="submenu-item ">
                    <a href="form-element-textarea.html">Textarea</a>
                </li>
            </ul>
        </li>

        <li class="sidebar-item  ">
            <a href="form-layout.html" class='sidebar-link'>
                <i class="bi bi-file-earmark-medical-fill"></i>
                <span>Form Layout</span>
            </a>
        </li>

        <li class="sidebar-item  has-sub">
            <a href="#" class='sidebar-link'>
                <i class="bi bi-pen-fill"></i>
                <span>Form Editor</span>
            </a>
            <ul class="submenu ">
                <li class="submenu-item ">
                    <a href="form-editor-quill.html">Quill</a>
                </li>
                <li class="submenu-item ">
                    <a href="form-editor-ckeditor.html">CKEditor</a>
                </li>
                <li class="submenu-item ">
                    <a href="form-editor-summernote.html">Summernote</a>
                </li>
                <li class="submenu-item ">
                    <a href="form-editor-tinymce.html">TinyMCE</a>
                </li>
            </ul>
        </li>

        <li class="sidebar-item  ">
            <a href="table.html" class='sidebar-link'>
                <i class="bi bi-grid-1x2-fill"></i>
                <span>Table</span>
            </a>
        </li>

        <li class="sidebar-item  has-sub">
            <a href="#" class='sidebar-link'>
                <i class="bi bi-file-earmark-spreadsheet-fill"></i>
                <span>Datatables</span>
            </a>
            <ul class="submenu ">
                <li class="submenu-item ">
                    <a href="table-datatable.html">Datatable</a>
                </li>
                <li class="submenu-item ">
                    <a href="table-datatable-jquery.html">Datatable (jQuery)</a>
                </li>
            </ul>
        </li>
    </ul>
</div>



<?php $this->endSection() ?>
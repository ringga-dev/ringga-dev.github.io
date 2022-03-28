<?php

namespace App\Controllers;

use App\Controllers\BaseController;

class AjaxView extends BaseController
{
    public function Ajax_menu()
    {
        $data = [
            'stts' => true,
            'msg' => 'menu loaded successfully',
            'data' => view('base_ui/menu/menu_view')
        ];

        echo json_encode($data);
    }
}

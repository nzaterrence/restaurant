odoo.define('flexibite_com_advance.floor', function (require) {
"use strict";

	var floors = require('pos_restaurant.floors')
	var models = require('point_of_sale.models');
	var rpc = require('web.rpc');
	var core = require('web.core');

	var _t = core._t;

	floors.FloorScreenWidget.include({
		show: function(){
	        this._super();
	        setTimeout(function(){
	        	$('#slidemenubtn').hide();
	        }, 10);
		},
	});

	floors.TableWidget.include({
        click_handler: function() {
            var self = this;
            var floorplan = this.getParent();
            if (floorplan.editing) {
                setTimeout(function() { // in a setTimeout to debounce with drag&drop start
                    if (!self.dragging) {
                        if (self.moved) {
                            self.moved = false;
                        } else if (!self.selected) {
                            self.getParent().select_table(self);
                        } else {
                            self.getParent().deselect_tables();
                        }
                    }
                }, 50);
            } else {
                if (this.table.parent_linked_table) {
                    floorplan.pos.set_table(this.table.parent_linked_table);
                } else {
                    floorplan.pos.set_table(this.table);
                }
            }
        },
        renderElement: function() {
            var self = this;
            if (!this.table.parent_linked_table) {
                this.table.parent_linked_table = this.pos.get_parent_linked_table(this.table)
            }
            this._super();
        },
    });

});
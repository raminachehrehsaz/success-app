classdef PatientsDisplay < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        PatientsDisplayUIFigure      matlab.ui.Figure
        Menu                         matlab.ui.container.Menu
        GridLayout                   matlab.ui.container.GridLayout
        LeftPanel                    matlab.ui.container.Panel
        NumofchildrenEditFieldLabel  matlab.ui.control.Label
        MainGroup                    matlab.ui.container.TabGroup
        MainTab                      matlab.ui.container.Tab
        EmployeeNameEditField        matlab.ui.control.EditField
        JoinUsDateEditField          matlab.ui.control.NumericEditField
        JoinUsDateEditFieldLabel     matlab.ui.control.Label
        ConsumerPageButton           matlab.ui.control.Button
        EmployeeNameEditFieldLabel   matlab.ui.control.Label
        ConsumerTab                  matlab.ui.container.Tab
        Product                      matlab.ui.container.Panel
        ProductDropDown              matlab.ui.control.DropDown
        InvestmentEditField          matlab.ui.control.NumericEditField
        InvestmentEditFieldLabel     matlab.ui.control.Label
        Gender                       matlab.ui.container.Panel
        MaleCheckBox                 matlab.ui.control.CheckBox
        FemaleCheckBox               matlab.ui.control.CheckBox
        MaritalStatus                matlab.ui.container.Panel
        SingleCheckBox               matlab.ui.control.CheckBox
        MarriedCheckBox              matlab.ui.control.CheckBox
        NumofchildrenEditField       matlab.ui.control.NumericEditField
        EducationButtonGroup         matlab.ui.container.ButtonGroup
        MastersdegreeButton          matlab.ui.control.ToggleButton
        BachelorsdegreeButton        matlab.ui.control.ToggleButton
        DiplomaButton                matlab.ui.control.ToggleButton
        Smoke                        matlab.ui.container.Panel
        YesCheckBox                  matlab.ui.control.CheckBox
        NoCheckBox                   matlab.ui.control.CheckBox
        RightPanel                   matlab.ui.container.Panel
        TabGroup                     matlab.ui.container.TabGroup
        Tab                          matlab.ui.container.Tab
        TextArea                     matlab.ui.control.TextArea
        TextAreaLabel                matlab.ui.control.Label
        Tab2                         matlab.ui.container.Tab
    end

    % Properties that correspond to apps with auto-reflow
    properties (Access = private)
        onePanelWidth = 576;
    end

    % The app displays the data by using the scatter plot, histogram, and table.
    % It makes use of tabs to separate the ploting options output from the table display of the data.
    % There are several graphical elements used such as checkboxes, slider, switch, dropdown, and radiobutton group.
    % The data used in the app is shipped with the product.
    
    properties (Access = private)
        % Declare properties of the PatientsDisplay class.
        Data
        SelectedGenders
        SelectedColors
        BinWidth
        Histogram = gobjects(0)
        displayedIndices
    end
    
    methods (Access = private)
        
        function NBins = numhistbins(app,data)
            % Utility function to compute the number of histogram bins 
            binwidth = app.BinWidth;
            range2plot =  floor(min(data)):binwidth:ceil(max(data));
            NBins = size(range2plot,2);
        end
        
        function annotateScatterPlot(app)
            % Update X and Y Labels
            app.Trend.XLabel.String = 'Weight';
            app.Trend.YLabel.String = app.BloodPressureSwitch.Value;
            % Dont show the histogram slider
            app.BinWidthSliderLabel.Visible = 'off';
            app.BinWidthSlider.Visible = 'off';
        end
        
        function annotateHistogram(app)
           
            % Update X and Y Labels
            app.Trend.XLabel.String = app.BloodPressureSwitch.Value;
            app.Trend.YLabel.String = '# of Patients';
            
            % Show histogram slider
            app.BinWidthSliderLabel.Visible = 'on';
            app.BinWidthSlider.Visible = 'on';
        end
        
        function filterData(app)
            % Utility function to filter the data according to the controls
            
            % Initially assume that all data will be displayed and then, subsequently, filter the data
            % based on the controls
            tempIndices = ones([size(app.Data,1),1]);
            
            % Append a column to tempIndices to indicate data that satisfies the smoker control
            if app.NoCheckBox.Value && ~app.YesCheckBox.Value
                tempIndices = [tempIndices, app.Data.Smoker == 0];
            elseif app.YesCheckBox.Value && ~app.NoCheckBox.Value
                tempIndices = [tempIndices, app.Data.Smoker == 1];
            elseif  ~app.YesCheckBox.Value && ~app.NoCheckBox.Value
                tempIndices = [tempIndices, zeros([size(app.Data,1),1])];
            end
            
            % Append a column to tempIndices to indicate data that satisfies the gender control
            if app.MaleCheckBox.Value && ~app.FemaleCheckBox.Value
                tempIndices = [tempIndices, app.Data.Gender == "Male"];
            elseif app.FemaleCheckBox.Value && ~app.MaleCheckBox.Value
                tempIndices = [tempIndices, app.Data.Gender == "Female"];
            elseif  ~app.FemaleCheckBox.Value && ~app.MaleCheckBox.Value
                tempIndices = [tempIndices, zeros([size(app.Data,1),1])];
            end
            
            % Append a column to tempIndices to indicate data that satisfies the location control
            if app.HospitalNameDropDown.Value ~= "All"
                tempIndices = [tempIndices, app.Data.Location == string(app.HospitalNameDropDown.Value)];
            end
            
            % Determine which data points satisfy all requirements
            app.displayedIndices = (sum(tempIndices,2)/size(tempIndices,2) == 1);
        end
    end

    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startupFcn(app)
            % Load the data.
            load('patients.mat','LastName','Gender','Smoker','Age','Height','Weight','Diastolic','Systolic','Location');
            
            % Store the data in a table and display it in one of the App's tabs.
            app.Data = table(LastName,app.Gender,Smoker,Age,Height,Weight,Diastolic,Systolic,Location);
            app.UITable.Data = app.Data;
            app.BinWidth = app.BinWidthSlider.Value;
            
            % Update the axes with the corresponding data.
            updateSelectedGenders(app)
            refreshplot(app)
        end

        % Changes arrangement of the app based on UIFigure width
        function updateAppLayout(app, event)
            currentFigureWidth = app.PatientsDisplayUIFigure.Position(3);
            if(currentFigureWidth <= app.onePanelWidth)
                % Change to a 2x1 grid
                app.GridLayout.RowHeight = {548, 548};
                app.GridLayout.ColumnWidth = {'1x'};
                app.RightPanel.Layout.Row = 2;
                app.RightPanel.Layout.Column = 1;
            else
                % Change to a 1x2 grid
                app.GridLayout.RowHeight = {'1x'};
                app.GridLayout.ColumnWidth = {284, '1x'};
                app.RightPanel.Layout.Row = 1;
                app.RightPanel.Layout.Column = 2;
            end
        end

        % Callback function
        function SliderValueChanging(app, event)
            % Update the histogram as the slider value for bindwidth changes.
            app.BinWidth = event.Value;
            for ii=1:length(app.Histogram)
                app.Histogram(ii).NumBins = numhistbins(app,app.Histogram(ii).Data);
            end
        end

        % Callback function
        function refreshplot(app, event)
            Genders = app.SelectedGenders;
            Colors = app.SelectedColors;
            
            % Start with a fresh plot
            cla(app.Trend)
            hold(app.Trend,'on')
            app.Histogram = gobjects(0);
            
            % Select relevant segment of data
            xdata = app.Data.Weight;
            ydata = app.Data.(app.BloodPressureSwitch.Value);
            
            % Filter the data according to the controls
            filterData(app);
            
            % Create either a scatter plot or histogram, based on selection
            switch app.EducationButtonGroup.SelectedObject.Text
                
                case 'Scatter'
                    % Build a scatter plot for each selected gender
                    for ii = 1:length(Genders)
                        selectedpatients = ((app.Data.Gender == Genders(ii)) & (app.displayedIndices));
                        scatter(app.Trend,xdata((selectedpatients)),ydata(selectedpatients),Colors{ii});
                    end
                    annotateScatterPlot(app)
                    
                case 'Histogram'
                    % Build a histogram for each selected gender
                    for ii = 1:length(Genders)
                        selectedpatients = ((app.Data.Gender == Genders(ii)) & (app.displayedIndices));
                        NBins = numhistbins(app,ydata(selectedpatients));
                        h = histogram(app.Trend,ydata(selectedpatients),NBins,'BinLimits',[floor(min(ydata)) ceil(max(ydata))]);
                        h.EdgeColor = Colors{ii};
                        h.FaceColor = Colors{ii};
                        app.Histogram = [app.Histogram h];
                    end
                    annotateHistogram(app)
                    
            end
            
            % Update the table to show only the data that satisfies the controls
            app.UITable.Data = app.Data(app.displayedIndices,:);
            drawnow;
        end

        % Value changed function: FemaleCheckBox, MaleCheckBox, 
        % ...and 2 other components
        function updateSelectedGenders(app, event)
            % List which genders and colors to use
            Genders = [];
            Colors = [];
            Smoker = [];
            
            if app.MaleCheckBox.Value
                Genders = "Male";
                Colors = "blue";
            end
            if app.FemaleCheckBox.Value
                Genders = [Genders "Female"];
                Colors = [Colors "red"];
            end
            if app.YesCheckBox.Value
                Smoker = "Yes";
            end
            if app.NoCheckBox.Value
                Smoker = [Smoker "No"];
            end
            
            if isempty(Genders) || isempty(Smoker)
                % Disable the switches and buttons if they were on
                app.BloodPressureSwitch.Enable = 'off';
                app.ScatterButton.Enable = 'off';
                app.HistogramButton.Enable = 'off';
                app.BinWidthSliderLabel.Enable = 'off';
                app.BinWidthSlider.Enable = 'off';
            else
                % Enable the switches and buttons if they were off
                app.BloodPressureSwitch.Enable = 'on';
                app.ScatterButton.Enable = 'on';
                app.HistogramButton.Enable = 'on';
                app.BinWidthSliderLabel.Enable = 'on';
                app.BinWidthSlider.Enable = 'on';
            end
            app.SelectedGenders = Genders;
            app.SelectedColors = Colors;
            
            refreshplot(app)
        end

        % Button down function: ConsumerTab
        function ConsumerTabButtonDown(app, event)
            app.MainGroup.SelectedTab = app.ConsumerTab;
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create PatientsDisplayUIFigure and hide until all components are created
            app.PatientsDisplayUIFigure = uifigure('Visible', 'off');
            app.PatientsDisplayUIFigure.AutoResizeChildren = 'off';
            app.PatientsDisplayUIFigure.Position = [100 100 701 548];
            app.PatientsDisplayUIFigure.Name = 'Patients Display';
            app.PatientsDisplayUIFigure.SizeChangedFcn = createCallbackFcn(app, @updateAppLayout, true);

            % Create Menu
            app.Menu = uimenu(app.PatientsDisplayUIFigure);
            app.Menu.Text = 'Menu';

            % Create GridLayout
            app.GridLayout = uigridlayout(app.PatientsDisplayUIFigure);
            app.GridLayout.ColumnWidth = {284, '1x'};
            app.GridLayout.RowHeight = {'1x'};
            app.GridLayout.ColumnSpacing = 0;
            app.GridLayout.RowSpacing = 0;
            app.GridLayout.Padding = [0 0 0 0];
            app.GridLayout.Scrollable = 'on';

            % Create LeftPanel
            app.LeftPanel = uipanel(app.GridLayout);
            app.LeftPanel.Layout.Row = 1;
            app.LeftPanel.Layout.Column = 1;
            app.LeftPanel.Scrollable = 'on';

            % Create Smoke
            app.Smoke = uipanel(app.LeftPanel);
            app.Smoke.AutoResizeChildren = 'off';
            app.Smoke.Title = 'Smoker';
            app.Smoke.Position = [7 13 100 97];

            % Create NoCheckBox
            app.NoCheckBox = uicheckbox(app.Smoke);
            app.NoCheckBox.ValueChangedFcn = createCallbackFcn(app, @updateSelectedGenders, true);
            app.NoCheckBox.Text = 'No';
            app.NoCheckBox.Position = [12 12 60 22];
            app.NoCheckBox.Value = true;

            % Create YesCheckBox
            app.YesCheckBox = uicheckbox(app.Smoke);
            app.YesCheckBox.ValueChangedFcn = createCallbackFcn(app, @updateSelectedGenders, true);
            app.YesCheckBox.Text = 'Yes';
            app.YesCheckBox.Position = [12 42 46 22];
            app.YesCheckBox.Value = true;

            % Create EducationButtonGroup
            app.EducationButtonGroup = uibuttongroup(app.LeftPanel);
            app.EducationButtonGroup.Title = 'Education';
            app.EducationButtonGroup.Position = [132 209 123 105];

            % Create DiplomaButton
            app.DiplomaButton = uitogglebutton(app.EducationButtonGroup);
            app.DiplomaButton.Text = 'Diploma';
            app.DiplomaButton.Position = [5 51 112 23];
            app.DiplomaButton.Value = true;

            % Create BachelorsdegreeButton
            app.BachelorsdegreeButton = uitogglebutton(app.EducationButtonGroup);
            app.BachelorsdegreeButton.Text = 'Bachelor''s degree';
            app.BachelorsdegreeButton.Position = [5 30 112 23];

            % Create MastersdegreeButton
            app.MastersdegreeButton = uitogglebutton(app.EducationButtonGroup);
            app.MastersdegreeButton.Text = 'Master''s degree';
            app.MastersdegreeButton.Position = [5 9 112 23];

            % Create NumofchildrenEditField
            app.NumofchildrenEditField = uieditfield(app.LeftPanel, 'numeric');
            app.NumofchildrenEditField.HorizontalAlignment = 'center';
            app.NumofchildrenEditField.Position = [221 172 48 22];

            % Create MaritalStatus
            app.MaritalStatus = uipanel(app.LeftPanel);
            app.MaritalStatus.AutoResizeChildren = 'off';
            app.MaritalStatus.Title = 'Marital Status';
            app.MaritalStatus.Position = [6 113 100 97];

            % Create MarriedCheckBox
            app.MarriedCheckBox = uicheckbox(app.MaritalStatus);
            app.MarriedCheckBox.Text = 'Married';
            app.MarriedCheckBox.Position = [12 8 63 22];

            % Create SingleCheckBox
            app.SingleCheckBox = uicheckbox(app.MaritalStatus);
            app.SingleCheckBox.Text = 'Single';
            app.SingleCheckBox.Position = [12 38 56 22];
            app.SingleCheckBox.Value = true;

            % Create Gender
            app.Gender = uipanel(app.LeftPanel);
            app.Gender.AutoResizeChildren = 'off';
            app.Gender.Title = 'Gender';
            app.Gender.Position = [7 217 100 97];

            % Create FemaleCheckBox
            app.FemaleCheckBox = uicheckbox(app.Gender);
            app.FemaleCheckBox.ValueChangedFcn = createCallbackFcn(app, @updateSelectedGenders, true);
            app.FemaleCheckBox.Text = 'Female';
            app.FemaleCheckBox.Position = [12 14 60 16];

            % Create MaleCheckBox
            app.MaleCheckBox = uicheckbox(app.Gender);
            app.MaleCheckBox.ValueChangedFcn = createCallbackFcn(app, @updateSelectedGenders, true);
            app.MaleCheckBox.Text = 'Male';
            app.MaleCheckBox.Position = [12 44 46 16];
            app.MaleCheckBox.Value = true;

            % Create MainGroup
            app.MainGroup = uitabgroup(app.LeftPanel);
            app.MainGroup.Position = [10 327 260 214];

            % Create MainTab
            app.MainTab = uitab(app.MainGroup);
            app.MainTab.Title = 'Main';

            % Create EmployeeNameEditFieldLabel
            app.EmployeeNameEditFieldLabel = uilabel(app.MainTab);
            app.EmployeeNameEditFieldLabel.HorizontalAlignment = 'right';
            app.EmployeeNameEditFieldLabel.Position = [5 153 94 22];
            app.EmployeeNameEditFieldLabel.Text = 'Employee Name';

            % Create ConsumerPageButton
            app.ConsumerPageButton = uibutton(app.MainTab, 'push');
            app.ConsumerPageButton.Position = [79 55 102 23];
            app.ConsumerPageButton.Text = 'Consumer Page';

            % Create JoinUsDateEditFieldLabel
            app.JoinUsDateEditFieldLabel = uilabel(app.MainTab);
            app.JoinUsDateEditFieldLabel.HorizontalAlignment = 'right';
            app.JoinUsDateEditFieldLabel.Position = [9 109 74 22];
            app.JoinUsDateEditFieldLabel.Text = 'Join Us Date';

            % Create JoinUsDateEditField
            app.JoinUsDateEditField = uieditfield(app.MainTab, 'numeric');
            app.JoinUsDateEditField.HorizontalAlignment = 'center';
            app.JoinUsDateEditField.Position = [103 109 152 22];

            % Create EmployeeNameEditField
            app.EmployeeNameEditField = uieditfield(app.MainTab, 'text');
            app.EmployeeNameEditField.Position = [106 153 149 22];

            % Create ConsumerTab
            app.ConsumerTab = uitab(app.MainGroup);
            app.ConsumerTab.Title = 'Consumer';
            app.ConsumerTab.ButtonDownFcn = createCallbackFcn(app, @ConsumerTabButtonDown, true);

            % Create Product
            app.Product = uipanel(app.ConsumerTab);
            app.Product.AutoResizeChildren = 'off';
            app.Product.Title = 'Product';
            app.Product.Position = [16 27 231 148];

            % Create InvestmentEditFieldLabel
            app.InvestmentEditFieldLabel = uilabel(app.Product);
            app.InvestmentEditFieldLabel.HorizontalAlignment = 'right';
            app.InvestmentEditFieldLabel.Position = [9 28 64 22];
            app.InvestmentEditFieldLabel.Text = 'Investment';

            % Create InvestmentEditField
            app.InvestmentEditField = uieditfield(app.Product, 'numeric');
            app.InvestmentEditField.HorizontalAlignment = 'center';
            app.InvestmentEditField.Position = [88 28 134 22];

            % Create ProductDropDown
            app.ProductDropDown = uidropdown(app.Product);
            app.ProductDropDown.Items = {'Finora/ Zarnova', 'Simazar', 'Andokhte dar', 'Omid Bazneshastegi'};
            app.ProductDropDown.Position = [11 82 201 22];
            app.ProductDropDown.Value = 'Finora/ Zarnova';

            % Create NumofchildrenEditFieldLabel
            app.NumofchildrenEditFieldLabel = uilabel(app.LeftPanel);
            app.NumofchildrenEditFieldLabel.HorizontalAlignment = 'right';
            app.NumofchildrenEditFieldLabel.Position = [113 172 96 22];
            app.NumofchildrenEditFieldLabel.Text = 'Num of children';

            % Create RightPanel
            app.RightPanel = uipanel(app.GridLayout);
            app.RightPanel.Layout.Row = 1;
            app.RightPanel.Layout.Column = 2;
            app.RightPanel.Scrollable = 'on';

            % Create TabGroup
            app.TabGroup = uitabgroup(app.RightPanel);
            app.TabGroup.Position = [14 113 376 404];

            % Create Tab
            app.Tab = uitab(app.TabGroup);
            app.Tab.Title = 'Tab';

            % Create TextAreaLabel
            app.TextAreaLabel = uilabel(app.Tab);
            app.TextAreaLabel.HorizontalAlignment = 'right';
            app.TextAreaLabel.Position = [21 286 55 22];
            app.TextAreaLabel.Text = 'Text Area';

            % Create TextArea
            app.TextArea = uitextarea(app.Tab);
            app.TextArea.Position = [91 8 273 302];

            % Create Tab2
            app.Tab2 = uitab(app.TabGroup);
            app.Tab2.Title = 'Tab2';

            % Show the figure after all components are created
            app.PatientsDisplayUIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = PatientsDisplay

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.PatientsDisplayUIFigure)

            % Execute the startup function
            runStartupFcn(app, @startupFcn)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.PatientsDisplayUIFigure)
        end
    end
end

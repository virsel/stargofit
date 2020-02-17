from django.urls import path
from .views import views
from .views import exercises
from .views import detail_and_manage_plan as plan
from django.contrib.auth.decorators import login_required
from .models import Exercise
from account.models import LikeDislike
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    # member training plan for list, edit, create and delete view
    path('change_favorites_list/', views.ChangeFavoritesListOfPlan,
         name='change_favorites_list'),
    path('send_data/', plan.SaveData,
         name='send_data'),
    path('change_current_plan_status/', views.ChangeCurrentPlanStatus,
         name='change_current_plan_status'),
    path('all_training_plans/', views.AllTraining_planList,
         name='all_training_plans'),


    # for displaying training_plans and exercise:

    path('', views.fFitnessStartPage, name='fitness'),


    # detail, edit, create, generate plan
    # detail
    path('training_plan_create/', plan.CreatePlanRequest,
         name='training_plan_create'),
    path('plan/<int:id>/<slug:slug>/', plan.TrainingPlanDetailView,
         name='training_plan_detail'),
    path('plan/training_data/', plan.fGetTrainingData,
         name='training_data'),
    # edit, create
    path('plan/delete_plan/', plan.DeletePlan,
         name='delete_plan'),
    path('plan/add_exercise/', plan.fAddExerciseToPlan,
         name='training_plan_add_exercise'),
    path('plan/change_areas_order/', plan.CheckIfMainAreasOrderIsChanged,
         name='training_plan_change_areas_order'),
    path('plan/change_day_of_all_trainings/', plan.ChangeDayOfAllTrainings,
         name='change_day_of_all_trainings'),
    path('plan/remove_exercise/', plan.fRemoveExerciseFromPlan,
         name='training_plan_remove_exercise'),
    path('plan/edit_sets/', plan.fEditTrainingSets,
         name='edit_sets'),
    path('plan/add_day/', plan.fEditAddTrainingDay,
         name='edit_add_day'),
    path('plan/change_training_kind/', plan.ChangeTrainingGoalRequest,
         name='edit_change_training_kind'),
    path('plan/add_day_label/', plan.fEditAddDayLabel,
         name='edit_add_day_label'),
    path('plan/input_changes/', plan.fEditInputChanges,
         name='edit_input_changes'),
    path('plan/order_changes/', plan.fEditOrderChanges,
         name='edit_order_changes'),
    path('plan/unit_order_changes/', plan.fEditUnitsOrderChanges,
         name='edit_unit_order_changes'),
    path('plan/delete_day/', plan.fEditDeleteDay,
         name='edit_delete_day'),
    # generate
    path('training_plan_generate/', plan.Training_planGenerate,
         name='training_plan_generate'),
    path('training_plan_generate/finish/', plan.Training_planGenerateFinish,
         name='training_plan_generate_finish'),
    # exercise selection
    path('exercises_dialog/', exercises.fGetExercisesDialog,
         name='exercises_dialog'),
    path('plan/exercise_selection_small_first/', exercises.ExerciseSelectionSmallWindowFirst,
         name='exercise_selection_small_first'),
    path('plan/exercise_selection_small_second/', exercises.ExerciseSelectionSmallWindowSecond,
         name='exercise_selection_small_second'),
    path('plan/exercise_selection_small_three/', exercises.ExerciseSelectionSmallWindowThird,
         name='exercise_selection_small_three'),
    # end detail, edit, create plan




    path('training_plan_create/search/selection/',
         plan.fGetExerciseBox, name='exercise_selection_box'),
    #    path('training_plan_create/set/',
    #         views.views.fGetExerciseSet, name='exercise_add_set'),
    #    path('training_plan_create/save/',
    #         views.views.fTrainingPlanCreateSave, name='exercise_create_save'),
    #    path('training_plan_create/new_circle/', views.views.fGetNewNumberCircle,
    #         name='training_plan_create_new_circle'),
    #    path('training_plan_create/', views.views.Training_planCreateView,
    #         name='training_plan_create'),






    # exercise detail
    path('exercise/<int:id>/<slug:slug>/',
         views.ExerciseDetailView, name='exercise_detail'),
    path('exercise/detail/rating',
         views.ExerciseRating, name='exercise_rating'),
    path('exercise_video', views.fGetExerciseVideo, name='exercise_video'),
    path('exercises/like/', login_required(views.VotesView.as_view(model=Exercise,
                                                                   vote_type=LikeDislike.like)), name='exercise_like'),
    path('exercises/dislike/', login_required(views.VotesView.as_view(model=Exercise,
                                                                      vote_type=LikeDislike.dislike)), name='exercise_dislike'),
    # end exercise detail



    # exercises
    path('all_exercises/', exercises.ExercisesListView, name='all_exercises'),
    path('exercises/selection/', exercises.fGetExercisesPerConditions,
         name='exercises_selection'),
    path('exercises/autocomplete/', exercises.fGetExercisesTitles,
         name='exercises_titles'),
    path('exercises/<slug:slug>/selection/',
         exercises.ExercisesListView, name='aeorobic'),
    # end exercises
]

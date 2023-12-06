

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a d)
(ontable b)
(on c h)
(ontable d)
(on e g)
(on f b)
(ontable g)
(ontable h)
(on i a)
(clear c)
(clear e)
(clear f)
(clear i)
)
(:goal
(and
(on b g)
(on c b)
(on e f)
(on f h)
(on g i)
(on i d))
)
)


